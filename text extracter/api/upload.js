export default async function handler(req, res) {
    if (req.method === 'POST') {
      // Handle OCR logic here
      return res.status(200).json({ text: 'Sample OCR result' });
    } else {
      res.status(405).end(); // Method Not Allowed
    }
  }
  