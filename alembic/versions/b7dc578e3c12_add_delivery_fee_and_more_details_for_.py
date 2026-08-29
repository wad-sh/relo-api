
"""add delivery fee and more details for driver application

Revision ID: b7dc578e3c12
Revises: d2cc7f61b1e8
Create Date: 2026-08-28 08:51:52.413323

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "b7dc578e3c12"
down_revision: Union[str, Sequence[str], None] = "d2cc7f61b1e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    bind = op.get_bind()

    # ---------------------------------------------------------
    # 1. Create new PostgreSQL ENUM types
    # ---------------------------------------------------------

    vehicle_type = postgresql.ENUM(
        "BICYCLE",
        "MOTORCYCLE",
        "CAR",
        "SUV",
        "VAN",
        "PICKUP_TRUCK",
        "TRUCK",
        "BUS",
        "OTHER",
        name="vehicletype",
    )

    application_status = postgresql.ENUM(
        "PENDING",
        "ACCEPTED",
        "REJECTED",
        name="applicationstatus",
    )

    assignment_status = postgresql.ENUM(
        "WAITING",
        "TAKEN",
        "EXPIRED",
        name="assignmentstatus",
    )

    vehicle_type.create(bind, checkfirst=True)
    application_status.create(bind, checkfirst=True)
    assignment_status.create(bind, checkfirst=True)

    # ---------------------------------------------------------
    # 2. Add new columns to drivers_applications
    # ---------------------------------------------------------

    op.add_column(
        "drivers_applications",
        sa.Column(
            "reviewed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "drivers_applications",
        sa.Column(
            "vehicle_type",
            vehicle_type,
            nullable=True,
        ),
    )

    op.add_column(
        "drivers_applications",
        sa.Column(
            "vehicle_model",
            sa.String(),
            nullable=True,
        ),
    )

    op.add_column(
        "drivers_applications",
        sa.Column(
            "vehicle_year",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "drivers_applications",
        sa.Column(
            "vehicle_capacity_kg",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "drivers_applications",
        sa.Column(
            "preferred_area",
            postgresql.ENUM(
                "HEBRON",
                "NABLUS",
                "RAMALLAH_AND_AL_BIREH",
                "JENIN",
                "BETHLEHEM",
                "JERICHO_AND_AL_AGHwar",
                "TULKARM",
                "QALQILYA",
                "SALFIT",
                "TUBAS_AND_NORTHERN_VALLEY",
                "JERUSALEM",
                name="governorate",
                create_type=False,
            ),
            nullable=True,
        ),
    )

    op.add_column(
        "drivers_applications",
        sa.Column(
            "preferred_route_from",
            postgresql.ENUM(
                "HEBRON",
                "NABLUS",
                "RAMALLAH_AND_AL_BIREH",
                "JENIN",
                "BETHLEHEM",
                "JERICHO_AND_AL_AGHwar",
                "TULKARM",
                "QALQILYA",
                "SALFIT",
                "TUBAS_AND_NORTHERN_VALLEY",
                "JERUSALEM",
                name="governorate",
                create_type=False,
            ),
            nullable=True,
        ),
    )

    op.add_column(
        "drivers_applications",
        sa.Column(
            "preferred_route_to",
            postgresql.ENUM(
                "HEBRON",
                "NABLUS",
                "RAMALLAH_AND_AL_BIREH",
                "JENIN",
                "BETHLEHEM",
                "JERICHO_AND_AL_AGHwar",
                "TULKARM",
                "QALQILYA",
                "SALFIT",
                "TUBAS_AND_NORTHERN_VALLEY",
                "JERUSALEM",
                name="governorate",
                create_type=False,
            ),
            nullable=True,
        ),
    )

    op.add_column(
        "drivers_applications",
        sa.Column(
            "description",
            sa.String(),
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # 3. Change drivers_applications.status ENUM
    # ---------------------------------------------------------

    # Convert old ENUM column to text first.
    op.execute(
        """
        ALTER TABLE drivers_applications
        ALTER COLUMN status TYPE text
        USING status::text
        """
    )

    # Remove old ENUM type.
    op.execute(
        """
        DROP TYPE IF EXISTS assignmenapplicationtstatus
        """
    )

    # Convert status values back to the new ENUM.
    op.execute(
        """
        ALTER TABLE drivers_applications
        ALTER COLUMN status TYPE applicationstatus
        USING status::applicationstatus
        """
    )

    # ---------------------------------------------------------
    # 4. Remove old drivers_applications columns/index
    # ---------------------------------------------------------

    op.drop_index(
        op.f("ix_drivers_applications_reviewed_by"),
        table_name="drivers_applications",
    )

    op.drop_column(
        "drivers_applications",
        "last_status_change",
    )

    # ---------------------------------------------------------
    # 5. Change drivers_assignments.status ENUM
    # ---------------------------------------------------------

    op.execute(
        """
        ALTER TABLE drivers_assignments
        ALTER COLUMN status TYPE text
        USING status::text
        """
    )

    op.execute(
        """
        ALTER TABLE drivers_assignments
        ALTER COLUMN status TYPE assignmentstatus
        USING (
            CASE status
                WHEN 'PENDING' THEN 'WAITING'
                WHEN 'ACCEPTED' THEN 'TAKEN'
                WHEN 'EXPIRED' THEN 'EXPIRED'
            END
        )::assignmentstatus
        """
    )

    # ---------------------------------------------------------
    # 6. responded_at should be nullable
    # ---------------------------------------------------------

    op.alter_column(
        "drivers_assignments",
        "responded_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
    )

    # ---------------------------------------------------------
    # 7. orders_history: changed_at -> created_at
    # ---------------------------------------------------------

    op.add_column(
        "orders_history",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    op.execute(
        """
        UPDATE orders_history
        SET created_at = now()
        WHERE created_at IS NULL
        """
    )

    op.alter_column(
        "orders_history",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
    )

    op.drop_column(
        "orders_history",
        "changed_at",
    )

    # ---------------------------------------------------------
    # 8. Make new driver application fields NOT NULL
    # ---------------------------------------------------------
    #
    # This is safe only if there are no existing rows in
    # drivers_applications.
    #
    # If existing rows exist, these columns must remain nullable
    # until those rows are populated.
    # ---------------------------------------------------------

    op.alter_column(
        "drivers_applications",
        "vehicle_type",
        existing_type=vehicle_type,
        nullable=False,
    )

    op.alter_column(
        "drivers_applications",
        "vehicle_model",
        existing_type=sa.String(),
        nullable=False,
    )

    op.alter_column(
        "drivers_applications",
        "vehicle_year",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.alter_column(
        "drivers_applications",
        "vehicle_capacity_kg",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.alter_column(
        "drivers_applications",
        "preferred_area",
        existing_type=postgresql.ENUM(
            "HEBRON",
            "NABLUS",
            "RAMALLAH_AND_AL_BIREH",
            "JENIN",
            "BETHLEHEM",
            "JERICHO_AND_AL_AGHwar",
            "TULKARM",
            "QALQILYA",
            "SALFIT",
            "TUBAS_AND_NORTHERN_VALLEY",
            "JERUSALEM",
            name="governorate",
            create_type=False,
        ),
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    # ---------------------------------------------------------
    # 1. Restore orders_history.changed_at
    # ---------------------------------------------------------

    op.add_column(
        "orders_history",
        sa.Column(
            "changed_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.drop_column(
        "orders_history",
        "created_at",
    )

    # ---------------------------------------------------------
    # 2. Restore drivers_assignments.status
    # ---------------------------------------------------------

    old_status = postgresql.ENUM(
        "PENDING",
        "ACCEPTED",
        "REJECTED",
        "EXPIRED",
        "ERROR",
        name="assignmenapplicationtstatus",
    )

    old_status.create(op.get_bind(), checkfirst=True)

    op.execute(
        """
        ALTER TABLE drivers_assignments
        ALTER COLUMN status TYPE text
        USING status::text
        """
    )

    op.execute(
        """
        ALTER TABLE drivers_assignments
        ALTER COLUMN status TYPE assignmenapplicationtstatus
        USING (
            CASE status
                WHEN 'WAITING' THEN 'PENDING'
                WHEN 'TAKEN' THEN 'ACCEPTED'
                WHEN 'EXPIRED' THEN 'EXPIRED'
            END
        )::assignmenapplicationtstatus
        """
    )

    op.alter_column(
        "drivers_assignments",
        "responded_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )

    # ---------------------------------------------------------
    # 3. Restore drivers_applications.status
    # ---------------------------------------------------------

    op.execute(
        """
        ALTER TABLE drivers_applications
        ALTER COLUMN status TYPE text
        USING status::text
        """
    )

    op.execute(
        """
        ALTER TABLE drivers_applications
        ALTER COLUMN status TYPE assignmenapplicationtstatus
        USING status::assignmenapplicationtstatus
        """
    )

    # ---------------------------------------------------------
    # 4. Restore old columns/index
    # ---------------------------------------------------------

    op.add_column(
        "drivers_applications",
        sa.Column(
            "last_status_change",
            postgresql.TIMESTAMP(timezone=True),
            nullable=True,
        ),
    )

    op.create_index(
        op.f("ix_drivers_applications_reviewed_by"),
        "drivers_applications",
        ["reviewed_by"],
        unique=False,
    )

    op.drop_column(
        "drivers_applications",
        "description",
    )

    op.drop_column(
        "drivers_applications",
        "preferred_route_to",
    )

    op.drop_column(
        "drivers_applications",
        "preferred_route_from",
    )

    op.drop_column(
        "drivers_applications",
        "preferred_area",
    )

    op.drop_column(
        "drivers_applications",
        "vehicle_capacity_kg",
    )

    op.drop_column(
        "drivers_applications",
        "vehicle_year",
    )

    op.drop_column(
        "drivers_applications",
        "vehicle_model",
    )

    op.drop_column(
        "drivers_applications",
        "vehicle_type",
    )

    op.drop_column(
        "drivers_applications",
        "reviewed_at",
    )

    # ---------------------------------------------------------
    # 5. Drop new ENUM types
    # ---------------------------------------------------------

    op.execute("DROP TYPE IF EXISTS assignmentstatus")
    op.execute("DROP TYPE IF EXISTS applicationstatus")
    op.execute("DROP TYPE IF EXISTS vehicletype")

