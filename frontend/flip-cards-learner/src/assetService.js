const S3_BASE = 'https://flipcards-app-assets.s3.eu-north-1.amazonaws.com';

export const getAssetUrl = (filename) => `${S3_BASE}/${filename}`;