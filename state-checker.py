import logging as log
import sys
import boto3
import botocore.exceptions

# Configurar logging
log.basicConfig(level=log.INFO)

class S3Manager:
    def __init__(self, region, bucket):
        self.region = region
        self.bucket = bucket
        self.s3 = boto3.resource('s3', region_name=self.region)
        self.s3_client = boto3.client('s3', region_name=self.region)

    def check_and_create_bucket(self):
        bucket = self.s3.Bucket(self.bucket)

        if bucket.creation_date:
            log.info(f"✅ El bucket '{self.bucket}' ya existe. No se necesita crear.")
        else:
            log.info(f"🚀 El bucket '{self.bucket}' no existe. Creando...")

            try:
                if self.region == "us-east-1":
                    self.s3_client.create_bucket(Bucket=self.bucket)
                else:
                    self.s3_client.create_bucket(
                        Bucket=self.bucket,
                        CreateBucketConfiguration={'LocationConstraint': self.region}
                    )
            except botocore.exceptions.ClientError as e:
                log.error(f"❌ Error al crear el bucket: {e}")
                sys.exit(1)

        # Activar versionado
        log.info(f"🔁 Habilitando versionado en el bucket '{self.bucket}'...")
        self.s3_client.put_bucket_versioning(
            Bucket=self.bucket,
            VersioningConfiguration={
                'Status': 'Enabled'
            }
        )

        # Verificar versionado
        versioning_status = self.s3_client.get_bucket_versioning(Bucket=self.bucket)
        log.info(f"🔍 Estado de versionado: {versioning_status.get('Status')}")

        # Bloquear acceso público
        log.info(f"🔐 Aplicando bloqueo de acceso público en el bucket '{self.bucket}'...")
        self.s3_client.put_public_access_block(
            Bucket=self.bucket,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )

        # Confirmar acceso público
        public_access = self.s3_client.get_public_access_block(Bucket=self.bucket)
        log.info(f"📛 Configuración de acceso público: {public_access['PublicAccessBlockConfiguration']}")


# === Script principal ===
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python state-checker.py <bucket-name>")
        sys.exit(1)

    bucket_name = sys.argv[1]
    region = "us-east-1"

    log.info(f"🔧 Bucket recibido: {bucket_name}")
    s3_mgr = S3Manager(region, bucket_name)
    s3_mgr.check_and_create_bucket()
