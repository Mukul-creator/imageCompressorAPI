# Image Processing API Documentation

This API provides functionality to compress images and add watermarks to them. Additionally, it offers a combined operation that both watermarks and compresses an image.

## Base URL
https://imagecompress.testbuddy.live

## Endpoints

### 1. `GET /hello`

A simple endpoint to test if the server is running.

**Response:**

- Status: `200 OK`
- Content: `"Hello, World!"`

---

### 2. `POST /api/compress`

Compresses an uploaded image using OpenCV.

**Request:**

- Method: `POST`
- Content-Type: `multipart/form-data`
- Parameters:
  - `image` (required): The image file to be compressed.
  - `quality` (optional): The quality of the compression (1-100). Default is `20`.
  - `downscale_factor` (optional): The factor by which the image is downscaled. Default is `2`.

**Response:**

- Status: `200 OK`
- Content: The compressed image as a JPEG file.

**Example Request:**

```bash
curl -X POST http://localhost:5000/api/compress \
  -F "image=@path_to_image/image.jpg" \
  -F "quality=30" \
  -F "downscale_factor=2"
## Endpoints
```

### 3. `POST /api/watermark`

Adds a watermark to an uploaded image.

**Request:**

- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `image` (required): The image file to add the watermark to.
  - `text` (required): The text to be used as the watermark.
  - `opacity` (optional): The opacity of the watermark (0.0 - 1.0). Default is `0.1`.

**Response:**

- **Status:** `200 OK`
- **Content:** The watermarked image as a JPEG file.

**Example Request:**

```bash
curl -X POST http://localhost:5000/api/watermark \
  -F "image=@path_to_image/image.jpg" \
  -F "text=Sample Watermark" \
  -F "opacity=0.2"
```

### 4. `POST /api/updateImage`

Combines both watermarking and compression in a single operation.

**Request:**

- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `image` (required): The image file to process.
  - `text` (required): The text to be used as the watermark.
  - `quality` (optional): The quality of the compression (1-100). Default is `20`.
  - `downscale_factor` (optional): The factor by which the image is downscaled. Default is `2`.
  - `opacity` (optional): The opacity of the watermark (0.0 - 1.0). Default is `0.1`.

**Response:**

- **Status:** `200 OK`
- **Content:** The processed image with both watermark and compression applied.

**Example Request:**

```bash
curl -X POST http://localhost:5000/api/updateImage \
  -F "image=@path_to_image/image.jpg" \
  -F "text=Sample Watermark" \
  -F "quality=30" \
  -F "downscale_factor=2" \
  -F "opacity=0.2"
