
# 🤖 JARVIS AI Assistant - Iron Man Edition

> Just A Rather Very Intelligent System - Your Personal AI Assistant with Iron Man Aesthetics

A cutting-edge AI assistant built with Streamlit, featuring Iron Man-inspired UI/UX and powered by Groq's lightning-fast LLM inference.

## ✨ Features

### 🎨 **Iron Man Themed Interface**
- **Arc Reactor Status Indicator** - Real-time system status visualization
- **Holographic Text Effects** - Futuristic typography and animations
- **Matrix Rain Background** - Animated code falling effect
- **Neural Network Visualization** - Live brain activity simulation
- **RGB Color Schemes** - Cyan, orange, and gold Iron Man palette

### 🧠 **Advanced AI Capabilities**
- **Lightning Fast Responses** - Powered by Groq's 0.3-0.8s inference
- **Context-Aware Conversations** - Remembers chat history
- **Intent Classification** - Smart routing for optimal response times
- **Multi-Source Responses** - Built-in + AI-powered responses

### 🚀 **Technical Features**
- **Modular Architecture** - Clean separation of concerns
- **Real-time System Monitoring** - CPU, memory, and network stats
- **Conversation Analytics** - Detailed interaction statistics
- **Export Functionality** - Save conversations as JSON
- **Error Handling** - Robust error recovery

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.9+
- Groq API Key (free at [console.groq.com](https://console.groq.com))

### **1. Clone Repository**

bash
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant

### **2. Install Dependencies**

bash
pip install -r requirements.txt

### **3. Configure API Key**

#### **Method A: Streamlit Secrets (Recommended)**
Create `.streamlit/secrets.toml`:

toml
GROQ_API_KEY = "gsk_your_groq_api_key_here"

#### **Method B: Environment Variable**

bash
export GROQ_API_KEY="gsk_your_groq_api_key_here"

#### **Method C: Direct Configuration**
Edit `config.py` and replace the placeholder API key.

### **4. Run Application**

bash
streamlit run app.py

## 🌐 Deployment

### **Streamlit Cloud**
1. Fork this repository
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Add `GROQ_API_KEY` to secrets
4. Deploy!

### **Docker Deployment**

dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


## 🎮 Usage Examples

### **Basic Interactions**

User: Hello JARVIS
JARVIS: Good day! JARVIS at your service. How may I assist you?

User: What is artificial intelligence?
JARVIS: Artificial intelligence is the simulation of human intelligence...


### **Technical Queries**

User: Explain quantum computing
JARVIS: Quantum computing harnesses quantum mechanical phenomena...

User: How do neural networks work?
JARVIS: Neural networks are computing systems inspired by biological...


### **Creative Tasks**

User: Write a poem about technology
JARVIS: In circuits bright and data streams...

User: Help me solve a complex problem
JARVIS: I'd be delighted to help you think through this...
