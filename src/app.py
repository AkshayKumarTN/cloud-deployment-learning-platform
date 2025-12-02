"""
DeployHub - Learn Cloud Deployment
A comprehensive guide to deploying web applications on various cloud platforms
"""

from flask import Flask, render_template_string, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
import time
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests',
                       ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds',
                            'HTTP request duration', ['method', 'endpoint'])

# Base styling
BASE_STYLE = '''
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        min-height: 100vh;
        color: white;
    }
    .navbar {
        background: rgba(0, 0, 0, 0.3);
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .navbar h1 { font-size: 1.5rem; }
    .nav-links { display: flex; gap: 2rem; flex-wrap: wrap; }
    .nav-links a {
        color: white;
        text-decoration: none;
        transition: opacity 0.3s;
    }
    .nav-links a:hover { opacity: 0.7; }
    .container {
        max-width: 1200px;
        margin: 2rem auto;
        padding: 0 2rem;
    }
    .content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
    }
    h1 { font-size: 2.5rem; margin-bottom: 1rem; }
    h2 { font-size: 1.8rem; margin: 2rem 0 1rem 0; color: #ffd700; }
    h3 { font-size: 1.3rem; margin: 1.5rem 0 0.5rem 0; }
    p, li { line-height: 1.8; margin-bottom: 1rem; }
    .step {
        background: rgba(0, 0, 0, 0.2);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .command {
        background: #2d2d2d;
        color: #0f0;
        padding: 1rem;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
        margin: 1rem 0;
        white-space: pre;
    }
    .note {
        background: rgba(255, 193, 7, 0.2);
        border-left: 4px solid #FFC107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    a { color: #ffd700; }
    ul { margin-left: 2rem; }
'''

# Home page template
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeployHub - Learn Cloud Deployment</title>
    <style>
        ''' + BASE_STYLE + '''
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .hero {
            text-align: center;
            padding: 3rem 0;
        }
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        .hero p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 2rem;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        .card h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #ffd700;
        }
        .card p { line-height: 1.6; color: rgba(255, 255, 255, 0.9); }
        .card a {
            display: inline-block;
            margin-top: 1rem;
            padding: 0.5rem 1.5rem;
            background: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .card a:hover { background: #45a049; }
        .icon { font-size: 3rem; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <nav class="navbar">
        <h1>🚀 DeployHub</h1>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/aws">AWS</a>
            <a href="/digitalocean">Digital Ocean</a>
            <a href="/docker">Docker</a>
            <a href="/cicd">CI/CD</a>
        </div>
    </nav>

    <div class="container">
        <div class="hero">
            <h1>Master Cloud Deployment</h1>
            <p>Learn to deploy web applications on AWS, Digital Ocean, and more</p>
        </div>

        <div class="cards">
            <div class="card">
                <div class="icon">☁️</div>
                <h3>AWS Deployment</h3>
                <p>Deploy your application on Amazon Web Services using EC2, RDS, and S3.</p>
                <a href="/aws">Learn AWS →</a>
            </div>

            <div class="card">
                <div class="icon">💧</div>
                <h3>Digital Ocean</h3>
                <p>Simple, developer-friendly cloud deployment with droplets and managed databases.</p>
                <a href="/digitalocean">Learn Digital Ocean →</a>
            </div>

            <div class="card">
                <div class="icon">🐳</div>
                <h3>Docker Containers</h3>
                <p>Containerize your application for consistent deployment anywhere.</p>
                <a href="/docker">Learn Docker →</a>
            </div>

            <div class="card">
                <div class="icon">⚙️</div>
                <h3>CI/CD Pipeline</h3>
                <p>Automate testing and deployment with GitHub Actions.</p>
                <a href="/cicd">Learn CI/CD →</a>
            </div>

            <div class="card">
                <div class="icon">📊</div>
                <h3>Monitoring</h3>
                <p>Track application health with Prometheus and Grafana.</p>
                <a href="/monitoring">Monitoring →</a>
            </div>

            <div class="card">
                <div class="icon">🧪</div>
                <h3>API Demo</h3>
                <p>Try our live API calculator endpoint.</p>
                <a href="/demo">Try Demo →</a>
            </div>
        </div>
    </div>
</body>
</html>
'''

DIGITALOCEAN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Digital Ocean Deployment - DeployHub</title>
    <style>
        ''' + BASE_STYLE + '''
        body { background: linear-gradient(135deg, #0080FF 0%, #0047AB 100%); }
    </style>
</head>
<body>
    <nav class="navbar">
        <h1>🚀 DeployHub</h1>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/aws">AWS</a>
            <a href="/digitalocean">Digital Ocean</a>
            <a href="/docker">Docker</a>
            <a href="/cicd">CI/CD</a>
        </div>
    </nav>

    <div class="container">
        <h1>💧 Digital Ocean Deployment Guide</h1>
        
        <div class="content">
            <h2>Overview</h2>
            <p>Digital Ocean provides simple, developer-friendly cloud infrastructure. Perfect for getting started with cloud deployment!</p>

            <div class="note">
                <strong>💡 Cost:</strong> Starting at $6/month for a basic droplet. $200 free credit for new users!
            </div>

            <h2>Step 1: Create Digital Ocean Account</h2>
            <div class="step">
                <h3>Sign Up</h3>
                <ul>
                    <li>Go to <a href="https://digitalocean.com">digitalocean.com</a></li>
                    <li>Sign up with email or GitHub</li>
                    <li>Verify email address</li>
                    <li>Add payment method</li>
                    <li>Get $200 free credit (new users)</li>
                </ul>
            </div>

            <h2>Step 2: Create a Droplet</h2>
            <div class="step">
                <h3>2.1 Choose Configuration</h3>
                <div class="command">Choose Image: Ubuntu 22.04 LTS
Choose Plan: Basic ($12/month - 2GB RAM)
Choose Region: Closest to you
Authentication: SSH Key (recommended)</div>
                
                <h3>2.2 SSH Key Setup</h3>
                <p>Generate SSH key on your local machine:</p>
                <div class="command">ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub</div>
                <p>Copy the output and add it to Digital Ocean</p>
            </div>

            <h2>Step 3: Connect to Your Droplet</h2>
            <div class="step">
                <div class="command">ssh root@YOUR_DROPLET_IP</div>
                <p>Replace YOUR_DROPLET_IP with your droplet's IP address</p>
            </div>

            <h2>Step 4: Install Docker</h2>
            <div class="step">
                <div class="command">apt update && apt upgrade -y
apt install -y docker.io docker-compose
systemctl start docker
systemctl enable docker</div>
            </div>

            <h2>Step 5: Deploy Your Application</h2>
            <div class="step">
                <h3>5.1 Clone Your Repository</h3>
                <div class="command">git clone https://github.com/username/your-repo.git
cd your-repo</div>
                
                <h3>5.2 Start with Docker Compose</h3>
                <div class="command">docker-compose up -d</div>
                
                <h3>5.3 Verify Deployment</h3>
                <div class="command">docker ps
curl http://localhost</div>
            </div>

            <h2>Step 6: Configure Firewall</h2>
            <div class="step">
                <div class="command">ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable</div>
            </div>

            <h2>Step 7: Set Up Monitoring</h2>
            <div class="step">
                <p>Access your monitoring dashboards:</p>
                <ul>
                    <li><strong>Prometheus:</strong> http://YOUR_IP:9090</li>
                    <li><strong>Grafana:</strong> http://YOUR_IP:3000</li>
                </ul>
            </div>

            <div class="note">
                <strong>✅ Success!</strong> Your application is now deployed on Digital Ocean with automated CI/CD!
            </div>

            <h2>Next Steps</h2>
            <ul>
                <li>Add a custom domain</li>
                <li>Set up SSL with Let's Encrypt</li>
                <li>Configure automated backups</li>
                <li>Set up monitoring alerts</li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

AWS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS Deployment - DeployHub</title>
    <style>
        ''' + BASE_STYLE + '''
        body { background: linear-gradient(135deg, #FF9900 0%, #FF6600 100%); }
    </style>
</head>
<body>
    <nav class="navbar">
        <h1>🚀 DeployHub</h1>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/aws">AWS</a>
            <a href="/digitalocean">Digital Ocean</a>
            <a href="/docker">Docker</a>
            <a href="/cicd">CI/CD</a>
        </div>
    </nav>

    <div class="container">
        <h1>☁️ AWS Deployment Guide</h1>
        
        <div class="content">
            <h2>Overview</h2>
            <p>Amazon Web Services (AWS) is the world's most comprehensive cloud platform with 200+ services.</p>

            <div class="note">
                <strong>💡 Free Tier:</strong> AWS offers 12 months free tier with t2.micro EC2 instances!
            </div>

            <h2>Step 1: Create AWS Account</h2>
            <div class="step">
                <ul>
                    <li>Visit <a href="https://aws.amazon.com">aws.amazon.com</a></li>
                    <li>Click "Create an AWS Account"</li>
                    <li>Provide email and password</li>
                    <li>Add payment method (required)</li>
                    <li>Choose Basic support plan (free)</li>
                </ul>
            </div>

            <h2>Step 2: Launch EC2 Instance</h2>
            <div class="step">
                <h3>2.1 Go to EC2 Dashboard</h3>
                <ul>
                    <li>Sign in to AWS Console</li>
                    <li>Search for "EC2" in services</li>
                    <li>Click "Launch Instance"</li>
                </ul>
                
                <h3>2.2 Configure Instance</h3>
                <div class="command">Name: my-web-server
AMI: Ubuntu Server 22.04 LTS
Instance type: t2.micro (Free tier eligible)
Key pair: Create new or use existing
Security group: Allow SSH (22), HTTP (80), HTTPS (443)</div>
            </div>

            <h2>Step 3: Connect to Instance</h2>
            <div class="step">
                <div class="command">chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP</div>
            </div>

            <h2>Step 4: Install Dependencies</h2>
            <div class="step">
                <div class="command">sudo apt update
sudo apt install -y docker.io docker-compose git
sudo usermod -aG docker ubuntu
sudo systemctl start docker</div>
            </div>

            <h2>Step 5: Deploy Application</h2>
            <div class="step">
                <div class="command">git clone https://github.com/username/repo.git
cd repo
docker-compose up -d</div>
            </div>

            <h2>Step 6: Configure Security Group</h2>
            <div class="step">
                <p>In AWS Console → EC2 → Security Groups:</p>
                <ul>
                    <li>Add inbound rule: HTTP (80) from 0.0.0.0/0</li>
                    <li>Add inbound rule: HTTPS (443) from 0.0.0.0/0</li>
                    <li>Add inbound rule: Custom TCP (3000, 9090) for monitoring</li>
                </ul>
            </div>

            <h2>Optional: Use Elastic IP</h2>
            <div class="step">
                <p>Allocate a static IP address:</p>
                <ul>
                    <li>Go to EC2 → Elastic IPs</li>
                    <li>Allocate new address</li>
                    <li>Associate with your instance</li>
                </ul>
            </div>

            <div class="note">
                <strong>✅ Success!</strong> Your application is running on AWS EC2!
            </div>
        </div>
    </div>
</body>
</html>
'''

DEMO_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Demo - DeployHub</title>
    <style>
        ''' + BASE_STYLE + '''
        body { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
        .api-demo {
            background: rgba(255, 255, 255, 0.15);
            padding: 2rem;
            border-radius: 10px;
            margin: 2rem 0;
        }
        input {
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
            border: none;
            width: 150px;
            font-size: 1rem;
        }
        button {
            padding: 10px 20px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            margin: 5px;
        }
        button:hover { background: #45a049; }
        #result {
            margin-top: 1rem;
            font-size: 1.5rem;
            font-weight: bold;
            color: #ffd700;
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <h1>🚀 DeployHub</h1>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/aws">AWS</a>
            <a href="/digitalocean">Digital Ocean</a>
            <a href="/docker">Docker</a>
            <a href="/cicd">CI/CD</a>
        </div>
    </nav>

    <div class="container">
        <h1>🧪 API Demo</h1>
        
        <div class="content">
            <h2>Live Calculator API</h2>
            <p>Test our REST API endpoint in real-time!</p>

            <div class="api-demo">
                <h3>Calculator</h3>
                <p>Enter two numbers to calculate their sum:</p>
                <input type="number" id="num1" placeholder="Number 1" value="5">
                <input type="number" id="num2" placeholder="Number 2" value="7">
                <button onclick="calculate()">Calculate Sum</button>
                <div id="result"></div>
            </div>

            <h2>How It Works</h2>
            <div class="step">
                <h3>API Endpoint</h3>
                <div class="command">POST /api/calculate
Content-Type: application/json

{
  "a": 5,
  "b": 7
}</div>
                
                <h3>Response</h3>
                <div class="command">{
  "result": 12,
  "operation": "5 + 7"
}</div>
            </div>

            <h2>Try It Yourself</h2>
            <div class="step">
                <p>Using curl:</p>
                <div class="command">curl -X POST http://YOUR_IP/api/calculate \\
  -H "Content-Type: application/json" \\
  -d '{"a": 5, "b": 7}'</div>
                
                <p>Using Python:</p>
                <div class="command">import requests

response = requests.post(
    'http://YOUR_IP/api/calculate',
    json={'a': 5, 'b': 7}
)
print(response.json())</div>
            </div>
        </div>
    </div>

    <script>
        function calculate() {
            const num1 = document.getElementById('num1').value;
            const num2 = document.getElementById('num2').value;
            
            fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({a: parseInt(num1), b: parseInt(num2)})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerHTML = 
                    `Result: ${num1} + ${num2} = ${data.result}`;
            })
            .catch(error => {
                document.getElementById('result').innerHTML = 
                    'Error: ' + error;
            });
        }
    </script>
</body>
</html>
'''

# Helper function
def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers"""
    return a + b

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    REQUEST_COUNT.labels(method=request.method,
                        endpoint=request.endpoint or 'unknown',
                        status=response.status_code).inc()
    REQUEST_DURATION.labels(method=request.method,
                           endpoint=request.endpoint or 'unknown').observe(duration)
    return response

@app.route('/')
def home():
    logger.info("Home page accessed")
    return render_template_string(HOME_TEMPLATE)

@app.route('/aws')
def aws():
    logger.info("AWS page accessed")
    return render_template_string(AWS_TEMPLATE)

@app.route('/digitalocean')
def digitalocean():
    logger.info("Digital Ocean page accessed")
    return render_template_string(DIGITALOCEAN_TEMPLATE)

@app.route('/docker')
def docker():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head><title>Docker Guide</title></head>
    <body style="background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); color: white; padding: 2rem;">
        <h1>🐳 Docker Guide - Coming Soon!</h1>
        <p><a href="/" style="color: white;">← Back to Home</a></p>
    </body>
    </html>
    ''')

@app.route('/cicd')
def cicd():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head><title>CI/CD Guide</title></head>
    <body style="background: linear-gradient(135deg, #E91E63 0%, #C2185B 100%); color: white; padding: 2rem;">
        <h1>⚙️ CI/CD Guide - Coming Soon!</h1>
        <p><a href="/" style="color: white;">← Back to Home</a></p>
    </body>
    </html>
    ''')

@app.route('/monitoring')
def monitoring():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head><title>Monitoring</title></head>
    <body style="background: linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%); color: white; padding: 2rem;">
        <h1>📊 Monitoring - Coming Soon!</h1>
        <p><a href="/" style="color: white;">← Back to Home</a></p>
    </body>
    </html>
    ''')

@app.route('/demo')
def demo():
    logger.info("Demo page accessed")
    return render_template_string(DEMO_TEMPLATE)

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    try:
        data = request.get_json()
        if not data or 'a' not in data or 'b' not in data:
            return jsonify({'error': 'Missing parameters'}), 400
        a = int(data['a'])
        b = int(data['b'])
        result = calculate_sum(a, b)
        logger.info(f"Calculation: {a} + {b} = {result}")
        return jsonify({'result': result, 'operation': f'{a} + {b}'})
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid input: {e}")
        return jsonify({'error': 'Invalid input'}), 400
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': 'Internal error'}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)