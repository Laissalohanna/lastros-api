"""create initial structure

Revision ID: 054f6d412241
Revises:
Create Date: 2026-03-03

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "054f6d412241"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # =========================
    # EXTENSION
    # =========================
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    # =========================
    # PROJECT
    # =========================
    op.create_table(
        "project",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("project_uid", sa.String(150), nullable=False, unique=True),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column("data", postgresql.JSONB),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.text("NOW()")
        ),
    )

    op.execute("""
        INSERT INTO project (project_uid, description, data)
        VALUES 
        (
            'crediffato/prd',
            'SANREMO FUNDO DE INVESTIMENTOS EM DIREITOS CREDITORIOS',
            '{
                "fund": {
                    "name": "SANREMO FIDC",
                    "document_number": "54.996.578/0001-79"
                },
                "architecture": "new_arch"
            }'::jsonb
        ),
        (
            'voxcred/bcard-prd',
            'VOX FUNDO DE INVESTIMENTO EM DIREITOS CREDITORIOS',
            '{
                "architecture": "new_arch"
            }'::jsonb
        );
    """)

    # =========================
    # STATUS_ENUM
    # =========================
    op.create_table(
        "status_enum",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("description", sa.String(100), nullable=False),
        sa.Column(
            "is_final", sa.Boolean, nullable=False, server_default=sa.text("false")
        ),
        sa.Column("active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.text("NOW()")
        ),
    )

    op.execute("""
        INSERT INTO status_enum (code, description, is_final)
        VALUES
        ('INSERTING', 'Inserindo dados na base', FALSE),
        ('INSERTED', 'Dados inseridos', FALSE),
        ('FETCHING_FILE', 'Buscando arquivo', FALSE),
        ('FILE_FETCHED', 'Arquivo obtido', FALSE),
        ('PROCESSING', 'Processando dados', FALSE),
        ('COMPLETED', 'Finalizado com sucesso', TRUE),
        ('FAILED', 'Falha no processamento', TRUE),
        ('CANCELLED', 'Processo cancelado', TRUE);
    """)

    # =========================
    # RECEIVABLE_TYPE
    # =========================
    op.create_table(
        "receivable_type",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("description", sa.String(100), nullable=False),
        sa.Column("configuration_data", postgresql.JSONB),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.text("NOW()")
        ),
    )

    # =========================
    # SEND_TYPE
    # =========================
    op.create_table(
        "send_type",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("description", sa.String(100), nullable=False),
        sa.Column("configuration_data", postgresql.JSONB),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.text("NOW()")
        ),
    )

    op.execute("""
        INSERT INTO send_type (code, description, configuration_data)
        VALUES
        (
            'AUTOMATIC',
            'Automático',
            '{
                "automatic": {
                    "enabled": true,
                    "schedule": {
                        "frequency": "daily",
                        "reference_date": {
                            "source": "system_date",
                            "offset": {
                                "unit": "days",
                                "value": -1
                            }
                        }
                    }
                }
            }'::jsonb
        ),
        (
            'PENDING_SPREADSHEET',
            'Planilha de pendências',
            '{
                "pending_spreadsheet": {
                    "enabled": false
                }
            }'::jsonb
        );
    """)

    # =========================
    # PATH_TYPE
    # =========================
    op.create_table(
        "path_type",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("description", sa.String(100), nullable=False),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.text("NOW()")
        ),
    )

    op.execute("""
        INSERT INTO path_type (code, description)
        VALUES
        ('BUCKET', 'Bucket'),
        ('GOOGLE_DRIVE', 'Google Drive'),
        ('SFTP', 'SFTP'),
        ('EMAIL', 'Email');
    """)

    # =========================
    # DESTINATARY
    # =========================
    op.create_table(
        "destinatary",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("configuration_data", postgresql.JSONB),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.text("NOW()")
        ),
    )

    op.execute("""
        INSERT INTO destinatary (name)
        VALUES
        ('QITECH'),
        ('EBOX'),
        ('INTERNAL'),
        ('H2');
    """)

    # =========================
    # BALLANTS
    # =========================
    op.create_table(
        "ballants",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column(
            "send_key", postgresql.UUID, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("transaction_uid", postgresql.UUID, nullable=False),
        sa.Column("unique_number_ccb", sa.String(150), nullable=False),
        sa.Column("your_number", sa.String(150)),
        sa.Column(
            "project_id", sa.BigInteger, sa.ForeignKey("project.id"), nullable=False
        ),
        sa.Column(
            "receivable_type_id",
            sa.Integer,
            sa.ForeignKey("receivable_type.id"),
            nullable=False,
        ),
        sa.Column("due_date", sa.Date),
        sa.Column("acquisition_date", sa.Date),
        sa.Column("data", postgresql.JSONB),
        sa.Column(
            "status_id", sa.Integer, sa.ForeignKey("status_enum.id"), nullable=False
        ),
        sa.Column(
            "send_type_id", sa.Integer, sa.ForeignKey("send_type.id"), nullable=False
        ),
        sa.Column(
            "path_type_id", sa.Integer, sa.ForeignKey("path_type.id"), nullable=False
        ),
        sa.Column("destinatary_id", sa.Integer, sa.ForeignKey("destinatary.id")),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.text("NOW()")
        ),
        sa.Column(
            "updated_at", sa.DateTime, nullable=False, server_default=sa.text("NOW()")
        ),
    )

    op.execute("""
        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trg_ballants_updated_at
        BEFORE UPDATE ON ballants
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at();
    """)

    op.create_index(
        "idx_ballants_project_transaction",
        "ballants",
        ["project_id", "transaction_uid"],
    )
    op.create_index("idx_ballants_status_id", "ballants", ["status_id"])
    op.create_index("idx_ballants_transaction_uid", "ballants", ["transaction_uid"])

    # =========================
    # BALLANT_EVENT_TYPE
    # =========================
    op.create_table(
        "ballant_event_type",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("description", sa.String(100), nullable=False),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.text("NOW()")
        ),
    )

    op.execute("""
        INSERT INTO ballant_event_type (code, description)
        VALUES
        ('CREATED', 'Registro do lastro criado'),
        ('STATUS_CHANGED', 'Status alterado'),
        ('SEND_ATTEMPT', 'Tentativa de envio'),
        ('SEND_SUCCESS', 'Envio realizado com sucesso'),
        ('SEND_FAILURE', 'Falha no envio'),
        ('DATA_VALIDATION_ERROR', 'Erro de validação'),
        ('MANUAL_UPDATE', 'Atualização manual');
    """)

    # =========================
    # BALLANT_EVENT
    # =========================
    op.create_table(
        "ballant_event",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column(
            "ballant_id",
            sa.BigInteger,
            sa.ForeignKey("ballants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "event_type_id",
            sa.Integer,
            sa.ForeignKey("ballant_event_type.id"),
            nullable=False,
        ),
        sa.Column("status_id", sa.Integer, sa.ForeignKey("status_enum.id")),
        sa.Column("message", sa.Text),
        sa.Column("metadata", postgresql.JSONB),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.text("NOW()")
        ),
    )

    op.create_index("idx_ballant_event_ballant_id", "ballant_event", ["ballant_id"])
    op.create_index("idx_ballant_event_created_at", "ballant_event", ["created_at"])


def downgrade():
    op.drop_index("idx_ballant_event_created_at", table_name="ballant_event")
    op.drop_index("idx_ballant_event_ballant_id", table_name="ballant_event")
    op.drop_table("ballant_event")

    op.drop_table("ballant_event_type")

    op.drop_index("idx_ballants_transaction_uid", table_name="ballants")
    op.drop_index("idx_ballants_status_id", table_name="ballants")
    op.drop_index("idx_ballants_project_transaction", table_name="ballants")

    op.execute("DROP TRIGGER IF EXISTS trg_ballants_updated_at ON ballants;")
    op.execute("DROP FUNCTION IF EXISTS set_updated_at;")

    op.drop_table("ballants")
    op.drop_table("destinatary")
    op.drop_table("path_type")
    op.drop_table("send_type")
    op.drop_table("receivable_type")
    op.drop_table("status_enum")
    op.drop_table("project")

    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
