
from pathlib import Path
import boto3
from botocore.config import Config

# Project configuration
PROJECT = Path("05-week-warehouse-storage")
ENV_FILE = PROJECT / ".env.minio"

SOURCE = Path("data/processed/nyc_taxi/partitioned")
BUCKET = "nyc-taxi-data"

# Read local credentials without displaying them
credentials = {}

for line in ENV_FILE.read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        key, value = line.split("=", 1)
        credentials[key.strip()] = value.strip()

# Connect to local MinIO S3 API
s3 = boto3.client(
    "s3",
    endpoint_url="http://127.0.0.1:9000",
    aws_access_key_id=credentials["MINIO_ROOT_USER"],
    aws_secret_access_key=credentials["MINIO_ROOT_PASSWORD"],
    region_name="us-east-1",
    config=Config(s3={"addressing_style": "path"}),
)

# Confirm bucket exists
s3.head_bucket(Bucket=BUCKET)
print(f"Connected to bucket: {BUCKET}")

# Find all Parquet files
files = sorted(SOURCE.rglob("*.parquet"))

if not files:
    raise FileNotFoundError("No partitioned Parquet files found!")

# Upload files with matching partition prefixes
for file in files:
    relative_path = file.relative_to(SOURCE)
    object_key = f"processed/{relative_path.as_posix()}"

    s3.upload_file(str(file), BUCKET, object_key)

    # Verify object exists and its size matches
    uploaded = s3.head_object(
        Bucket=BUCKET,
        Key=object_key,
    )

    assert uploaded["ContentLength"] == file.stat().st_size

    print(f"Uploaded and verified: {object_key}")

print(f"\nSuccessfully uploaded {len(files)} Parquet files!")
