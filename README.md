# Freepik FastMCP Toolkit

🚀 **MCP Server for seamless Freepik API integration**

## 🎯 What is this?

A **Model Context Protocol (MCP) server** that connects your AI assistants (Claude, Cursor, etc.) directly with Freepik's powerful APIs. Generate, search, and manage visual content without leaving your AI workflow.

<a href="https://glama.ai/mcp/servers/@freepik-company/freepik-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@freepik-company/freepik-mcp/badge" alt="Freepik FastToolkit MCP server" />
</a>

## 🛠️ What tools are available?

- 🎨 **Icon Search & Download** - Find and download icons in multiple formats
- 📁 **Resource Management** - Access and manage multimedia content  
- 🤖 **AI Image Classification** - Automatically classify and analyze images
- 🖼️ **Image Generation** - Create custom images using Mystic AI

## 📋 Prerequisites

Before you start, make sure you have:

- **Python 3.12+** installed
- **uv** dependency manager ([install here](https://docs.astral.sh/uv/getting-started/installation/))
- **Freepik API Key** ([get yours here](https://freepik.com/api))

## 🚀 Installation

### 1. Clone and navigate
```bash
git clone <REPOSITORY_URL>
cd freepik-toolkit/fastmcp
```

### 2. Install using Makefile
```bash
# Install dependencies
make install

# Verify installation
make version
```

### 3. Configure your API Key
```bash
echo "FREEPIK_API_KEY=your_api_key_here" > .env
```

> 💡 **Get your API Key at:** [freepik.com/api](https://freepik.com/api)

## ⚙️ Configuration for AI Assistants

### For Claude Desktop or Cursor on Linux

Add this to your `config.json` file:

> ⚠️ **For Windows users:** If you're on Windows, you need to use WSL (Windows Subsystem for Linux) to run this MCP server.

```json
{
  "mcpServers": {
    "freepik-fastmcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory", 
        "/FULL/PATH/TO/freepik-mcp",
        "fastmcp",
        "run",
        "main.py"
      ],
      "env": {
        "FREEPIK_API_KEY": "your_actual_api_key_here"
      }
    }
  }
}
```

### 🔧 Important Configuration Steps

1. **Find your full path:**
   ```bash
   pwd
   # Copy the output and replace /FULL/PATH/TO/ in the config
   ```

2. **Replace with your API key:**
   - Get it from [freepik.com/api](https://freepik.com/api)
   - Replace `your_actual_api_key_here`

## 🏃‍♂️ Quick Start

```bash
# Development mode (auto-reload)
make dev

# Production mode  
make run

# Check code quality
make lint

# Format code
make format

# Clean temporary files
make clean

# See all commands
make help
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### 📝 Commit Convention

This project uses **Conventional Commits**. Format your commits as:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix  
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(icons): add search filtering by category
fix(api): resolve authentication timeout issue  
docs(readme): update installation instructions
refactor(mystic): improve error handling logic
```

### 🔄 Contribution Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feat/amazing-feature`
3. **Commit** using conventional format: `git commit -m "feat: add amazing feature"`
4. **Push** to your branch: `git push origin feat/amazing-feature`
5. **Open** a Pull Request

## 📚 Development Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install dependencies |
| `make dev` | Run in development mode |
| `make run` | Run in production mode |
| `make lint` | Check code quality |
| `make format` | Format code automatically |
| `make clean` | Clean temporary files |
| `make version` | Check FastMCP version |

## 🛡️ Security

- ⚠️ **Never commit your API Key**
- ✅ Use `.env` files for sensitive data
- ✅ The `.env` file is in `.gitignore`

## 📖 API Documentation

For detailed API information:
- [Freepik API Documentation](https://freepik.com/api)

## 🆘 Troubleshooting

**Common issues:**

1. **"Command not found"** → Install `uv` dependency manager
2. **"Invalid API Key"** → Check your key at [freepik.com/api](https://freepik.com/api)
3. **"Path not found"** → Verify the full path in your config
4. **"Connection refused"** → Make sure the server is running with `make dev`

**Still having issues?** Open an issue on GitHub with:
- Your OS and Python version
- Full error message
- Configuration file (without API key)

---

**Ready to create amazing content with AI? 🎨✨** 