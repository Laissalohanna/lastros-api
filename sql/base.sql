-- =========================================
-- EXTENSÃO PARA UUID
-- =========================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================================
-- PROJECT
-- =========================================
CREATE TABLE project (
    id BIGSERIAL PRIMARY KEY,
    project_uid VARCHAR(150) NOT NULL UNIQUE,
    description VARCHAR(255) NOT NULL,
    data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO project (project_uid, description)
VALUES 
    ('crediffato/prd', 'SANREMO FUNDO DE INVESTIMENTOS EM DIREITOS CREDITORIOS','{
  "fund": {
    "name": "SANREMO FIDC",
    "document_number": "54.996.578/0001-79" 
  }
}'),
    ('voxcred/bcard-prd', 'VOX FUNDO DE INVESTIMENTO EM DIREITOS CREDITORIOS', '{}');

-- =========================================
-- STATUS_ENUM
-- =========================================
CREATE TABLE status_enum (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(100) NOT NULL,
    is_final BOOLEAN NOT NULL DEFAULT FALSE,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO status_enum (code, description, is_final, active)
VALUES
    ('DOWNLOADING', 'Baixando arquivo', FALSE, TRUE),
    ('DOWNLOADED', 'Arquivo baixado', FALSE, TRUE),
    ('WAITING_SEND', 'Aguardando envio', FALSE, TRUE),
    ('SENT', 'Enviado', TRUE, TRUE),
    ('FAILED', 'Falha', TRUE, TRUE),
    ('CANCELLED', 'Cancelado', TRUE, TRUE);

-- =========================================
-- RECEIVABLE_TYPE
-- =========================================
CREATE TABLE receivable_type (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(100) NOT NULL,
    configuration_data JSONB, 
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO receivable_type (code, description)
VALUES
    ('CCB', 'CCB', '{
  "file_search": {
    "search_parameter": "unique_number_ccb",
    "expected_name": true,
    "name_format": "{search_parameter}.pdf.p7s",
    "bucket_path": "{s3_folder}/{transaction_uid}/bcard_banking/ccb/",
    "archive_format": ".p7s"
  }
}' ),
    ('DEBT_CONFESSION', 'Confissão de dívida', '{
  "file_search": {
    "search_parameter": "unique_number_ccb",
    "expected_name": false,
    "bucket_path": "{s3_folder}/{transaction_uid}/docs/convertFilePart/index-0/pdf-0/",
    "archive_format": ".p7s"
  }
}'),
    ('CREDIT_CARD_INVOICE', 'Fatura de CARTÃO DE CRÉDITO', '{
  "file_search": {
    "search_parameter": "your_number",
    "expected_name": false,
    "bucket_path": "{s3_folder}/{transaction_uid}/docs/convertFilePart/index-0/pdf-0/",
    "archive_format": ".p7s"
  }
}');

-- =========================================
-- SEND_TYPE
-- =========================================
CREATE TABLE send_type (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(100) NOT NULL,
    configuration_data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO send_type (code, description)
VALUES
    ('AUTOMATIC', 'Automático','{
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
}'),
    ('PENDING_SPREADSHEET', 'Planilha de pendências','{
  "pending_spreadsheet": {
    "enabled": false
  }
}');

-- =========================================
-- PATH_TYPE
-- =========================================
CREATE TABLE path_type (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO path_type (code, description)
VALUES
    ('BUCKET', 'Bucket'),
    ('GOOGLE_DRIVE', 'Google Drive'),
    ('SFTP', 'SFTP'),
    ('EMAIL', 'EMAIL');

-- =========================================
-- DESTINATARY (com configuração JSONB)
-- =========================================
CREATE TABLE destinatary (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    configuration_data JSONB, 
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO destinatary (name)
VALUES
    ('QITECH'),
    ('EBOX'),
    ('INTERNAL'),
    ('H2');

-- =========================================
-- BALLANTS
-- =========================================
CREATE TABLE ballants (
    id BIGSERIAL PRIMARY KEY,

    send_key UUID NOT NULL UNIQUE,
    transaction_uid UUID,

    unique_number_ccb VARCHAR(150) NOT NULL,
    your_number VARCHAR(150),

    project_id BIGINT NOT NULL
        REFERENCES project(id),

    receivable_type_id INT NOT NULL
        REFERENCES receivable_type(id),

    due_date DATE,
    acquisition_date DATE,

    data JSONB, -- metadata variável (archive_name, search_status)

    status_id INT NOT NULL
        REFERENCES status_enum(id),

    send_type_id INT NOT NULL
        REFERENCES send_type(id),

    path_type_id INT NOT NULL
        REFERENCES path_type(id),

    destinatary_id INT
        REFERENCES destinatary(id), 

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- =========================================
-- ÍNDICE COMPOSTO PRINCIPAL
-- =========================================
CREATE INDEX idx_ballants_project_transaction_ccb
ON ballants (
    project_id,
    transaction_uid,
    unique_number_ccb
);

CREATE INDEX idx_ballants_status_id ON ballants(status_id);
CREATE INDEX idx_ballants_project_id ON ballants(project_id);

-- =========================================
-- BALLANT_EVENT_TYPE
-- =========================================
CREATE TABLE ballant_event_type (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);


INSERT INTO ballant_event_type (code, description)
VALUES
    ('CREATED', 'Registro do lastro criado'),
    ('STATUS_DOWNLOADING', 'Status alterado para DOWNLOADING'),
    ('STATUS_DOWNLOADED', 'Status alterado para DOWNLOADED'),
    ('STATUS_WAITING_SEND', 'Status alterado para WAITING_SEND'),
    ('STATUS_SENT', 'Status alterado para SENT'),
    ('STATUS_FAILED', 'Status alterado para FAILED'),
    ('STATUS_CANCELLED', 'Status alterado para CANCELLED'),
    ('SEND_ATTEMPT', 'Tentativa de envio do lastro'),
    ('SEND_SUCCESS', 'lastro enviado com sucesso'),
    ('SEND_FAILURE', 'Falha no envio do lastro'),
    ('DATA_VALIDATION_ERROR', 'Erro na validação dos dados do lastro'),
    ('MANUAL_UPDATE', 'Atualização manual do lastro');

-- =========================================
-- BALLANT_EVENT
-- =========================================
CREATE TABLE ballant_event (
    id BIGSERIAL PRIMARY KEY,

    ballant_id BIGINT NOT NULL
        REFERENCES ballants(id) ON DELETE CASCADE,

    event_type_id INT NOT NULL
        REFERENCES ballant_event_type(id),

    status_id INT
        REFERENCES status_enum(id),

    message TEXT,
    metadata JSONB,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ballant_event_ballant_id
    ON ballant_event(ballant_id);

CREATE INDEX idx_ballant_event_created_at
    ON ballant_event(created_at);