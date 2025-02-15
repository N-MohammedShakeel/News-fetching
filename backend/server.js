const express = require("express");
const cors = require("cors");
const axios = require("axios");
const path = require("path");

const app = express();
app.use(cors());

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname, "public")));

const GITHUB_RAW_URL =
  "https://raw.githubusercontent.com/N-MohammedShakeel/News-fetching/main/news.json";

app.get("/news", async (req, res) => {
  try {
    const response = await axios.get(GITHUB_RAW_URL);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch news" });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
