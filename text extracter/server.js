const express = require('express');
const path = require('path');
const multer = require('multer');
const session = require('express-session');
const { execFile } = require('child_process');
const fs = require('fs');

const app = express();

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
  secret: 'mysecretkey',
  resave: false,
  saveUninitialized: true
}));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

const upload = multer({ dest: 'uploads/' });

// Routes
app.get('/', (req, res) => {
  res.render('upload', { userid: req.session.userid });
});

app.get('/login', (req, res) => {
  res.render('login', { error: null });
});

app.post('/login', (req, res) => {
  const { userid, password } = req.body;
  if (userid === 'rajeev' && password === '11112003') {
    req.session.userid = userid;
    res.render('login-success', { userid });
  } else {
    res.render('login', { error: 'Invalid credentials. Try again.' });
  }
});

app.post('/upload', upload.single('inputFile'), (req, res) => {
  const { cameraImage } = req.body;

  const handlePythonResult = (imagePath) => {
    execFile('python', ['model.py', imagePath], (error, stdout, stderr) => {
      if (error) {
        console.error('Python error:', error);
        console.error('Stderr:', stderr);
        console.error('Stdout:', stdout);
        return res.status(500).send('Error processing the image.');
      }

      try {
        const result = JSON.parse(stdout);  // Parse the JSON output from the Python script

        // Only send back the custom model result
        res.render('result', {
          custom_model: result.custom_model || '(No custom model output)',
          error: result.error || null
        });
      } catch (err) {
        console.error('JSON parse error:', err);
        console.error('Raw stdout:', stdout);
        return res.status(500).send('Failed to parse OCR results.');
      }
    });
  };

  if (cameraImage && cameraImage.startsWith('data:image/')) {
    const base64Data = cameraImage.replace(/^data:image\/\w+;base64,/, '');
    const buffer = Buffer.from(base64Data, 'base64');
    const filename = `uploads/camera_${Date.now()}.png`;

    fs.writeFile(filename, buffer, (err) => {
      if (err) return res.status(500).send('Failed to save captured image.');
      handlePythonResult(filename);
    });

  } else if (req.file) {
    const imagePath = path.join(__dirname, req.file.path);
    handlePythonResult(imagePath);
  } else {
    return res.status(400).send('No image provided.');
  }
});


// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
