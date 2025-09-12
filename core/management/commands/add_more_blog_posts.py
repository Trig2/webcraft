from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random

from core.models import BlogTag, BlogPost


class Command(BaseCommand):
    help = "Add 20 more comprehensive blog posts"

    def handle(self, *args, **options):
        self.stdout.write("Adding 20 more blog posts...")

        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                "admin", "admin@webbuilder.com", "admin123"
            )

        # Create additional tags if needed
        additional_tags_data = [
            ("API Development", "#FF6B6B"),
            ("Cloud Computing", "#4ECDC4"),
            ("DevOps", "#45B7D1"),
            ("Machine Learning", "#96CEB4"),
            ("Cybersecurity", "#FFEAA7"),
            ("Mobile Development", "#DDA0DD"),
            ("Database Design", "#98D8C8"),
            ("Testing", "#F7DC6F"),
            ("Microservices", "#BB8FCE"),
            ("Blockchain", "#85C1E9"),
        ]

        for name, color in additional_tags_data:
            tag, created = BlogTag.objects.get_or_create(
                name=name, defaults={"color": color}
            )
            if created:
                self.stdout.write(f"Created tag: {name}")

        # Blog posts data
        posts_data = [
            {
                "title": "Building RESTful APIs with Django REST Framework",
                "excerpt": "Learn how to create robust and scalable APIs using Django REST Framework with authentication, pagination, and best practices.",
                "content": """
<h2>Introduction to Django REST Framework</h2>
<p>Django REST Framework (DRF) is a powerful toolkit for building Web APIs in Django. It provides a rich set of features for creating RESTful services that are both robust and maintainable.</p>

<h3>Setting Up Your First API</h3>
<p>Start by installing Django REST Framework and configuring your settings. Here's what you need to know:</p>

<h4>Installation</h4>
<pre><code>pip install djangorestframework</code></pre>

<h3>Creating Serializers</h3>
<p>Serializers in DRF allow complex data types, such as querysets and model instances, to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types.</p>

<h3>ViewSets and Routers</h3>
<p>ViewSets provide a set of views in a single class, while routers provide an easy way of automatically determining the URL conf.</p>

<h3>Authentication and Permissions</h3>
<p>Implement proper authentication using Token Authentication, Session Authentication, or JWT tokens for secure API access.</p>

<h3>Best Practices</h3>
<ul>
    <li>Use proper HTTP status codes</li>
    <li>Implement pagination for large datasets</li>
    <li>Add proper error handling</li>
    <li>Document your API with tools like Swagger</li>
    <li>Version your APIs for backward compatibility</li>
</ul>
                """,
                "tags": ["Django", "API Development", "Web Development"],
                "is_featured": True,
            },
            {
                "title": "Modern CSS Grid vs Flexbox: When to Use Which",
                "excerpt": "A comprehensive comparison of CSS Grid and Flexbox, helping you choose the right layout method for your projects.",
                "content": """
<h2>Understanding Layout Systems</h2>
<p>CSS provides multiple layout systems, with Grid and Flexbox being the most powerful and modern approaches for creating responsive layouts.</p>

<h3>CSS Grid: Two-Dimensional Layouts</h3>
<p>CSS Grid excels at creating complex, two-dimensional layouts where you need control over both rows and columns.</p>

<h4>When to Use Grid:</h4>
<ul>
    <li>Creating page layouts with header, sidebar, main content, and footer</li>
    <li>Building complex card layouts</li>
    <li>Aligning items in both dimensions simultaneously</li>
</ul>

<h3>Flexbox: One-Dimensional Layouts</h3>
<p>Flexbox is perfect for one-dimensional layouts, either in a row or column direction.</p>

<h4>When to Use Flexbox:</h4>
<ul>
    <li>Navigation bars and menus</li>
    <li>Centering content</li>
    <li>Distributing space between items</li>
    <li>Creating responsive component layouts</li>
</ul>

<h3>Combining Both</h3>
<p>The most powerful approach is using Grid for page layout and Flexbox for component layout within grid items.</p>
                """,
                "tags": ["CSS3", "UI/UX Design", "Web Development"],
                "is_featured": False,
            },
            {
                "title": "Introduction to Machine Learning for Web Developers",
                "excerpt": "Explore how web developers can integrate machine learning into their applications using Python and JavaScript frameworks.",
                "content": """
<h2>Machine Learning Meets Web Development</h2>
<p>Machine learning is no longer exclusive to data scientists. Web developers can now integrate ML capabilities into their applications.</p>

<h3>Getting Started with TensorFlow.js</h3>
<p>TensorFlow.js allows you to run machine learning models directly in the browser or Node.js applications.</p>

<h3>Python Integration</h3>
<p>Use Django or Flask to create ML-powered APIs that serve predictions to your frontend applications.</p>

<h3>Common Use Cases</h3>
<ul>
    <li>Image classification and recognition</li>
    <li>Natural language processing</li>
    <li>Recommendation systems</li>
    <li>Predictive analytics</li>
    <li>Chatbots and virtual assistants</li>
</ul>

<h3>Tools and Libraries</h3>
<p>Popular tools include scikit-learn, TensorFlow, PyTorch, and various pre-trained models available through APIs.</p>
                """,
                "tags": ["Machine Learning", "Python", "JavaScript"],
                "is_featured": True,
            },
            {
                "title": "Securing Your Web Applications: A Developer's Guide",
                "excerpt": "Essential security practices every web developer should implement to protect their applications and users.",
                "content": """
<h2>Web Application Security Fundamentals</h2>
<p>Security should be built into your application from the ground up, not added as an afterthought.</p>

<h3>OWASP Top 10 Vulnerabilities</h3>
<p>Understanding and preventing the most common security vulnerabilities:</p>

<h4>1. Injection Attacks</h4>
<p>SQL injection, XSS, and command injection prevention techniques.</p>

<h4>2. Authentication and Session Management</h4>
<p>Implementing secure authentication with proper session handling.</p>

<h3>Best Practices</h3>
<ul>
    <li>Use HTTPS everywhere</li>
    <li>Implement proper input validation</li>
    <li>Use parameterized queries</li>
    <li>Keep software updated</li>
    <li>Implement proper error handling</li>
</ul>

<h3>Security Headers</h3>
<p>Configure security headers like CSP, HSTS, and X-Frame-Options to protect against common attacks.</p>
                """,
                "tags": ["Cybersecurity", "Web Development", "Security"],
                "is_featured": False,
            },
            {
                "title": "Building Progressive Web Apps (PWAs) in 2025",
                "excerpt": "Learn how to create app-like experiences on the web with service workers, offline functionality, and native features.",
                "content": """
<h2>The Power of Progressive Web Apps</h2>
<p>PWAs bridge the gap between web and native applications, offering app-like experiences with web technologies.</p>

<h3>Core PWA Features</h3>
<ul>
    <li>Offline functionality with service workers</li>
    <li>Push notifications</li>
    <li>App-like interface</li>
    <li>Installation on device home screen</li>
</ul>

<h3>Service Workers</h3>
<p>Service workers enable offline functionality and background sync, making your app work even without internet connection.</p>

<h3>Web App Manifest</h3>
<p>The manifest file defines how your app appears when installed on a user's device.</p>

<h3>Performance Optimization</h3>
<p>PWAs must be fast and responsive. Implement lazy loading, code splitting, and efficient caching strategies.</p>
                """,
                "tags": ["PWA", "JavaScript", "Mobile Development"],
                "is_featured": True,
            },
            {
                "title": "Microservices Architecture with Docker and Kubernetes",
                "excerpt": "Design and deploy scalable microservices using containerization and orchestration tools.",
                "content": """
<h2>Breaking Down Monoliths</h2>
<p>Microservices architecture allows you to build applications as a collection of loosely coupled services.</p>

<h3>Benefits of Microservices</h3>
<ul>
    <li>Independent deployment</li>
    <li>Technology diversity</li>
    <li>Fault isolation</li>
    <li>Scalability</li>
</ul>

<h3>Containerization with Docker</h3>
<p>Docker containers provide consistent environments across development, testing, and production.</p>

<h3>Orchestration with Kubernetes</h3>
<p>Kubernetes manages containerized applications at scale, providing service discovery, load balancing, and auto-scaling.</p>

<h3>Best Practices</h3>
<ul>
    <li>Design for failure</li>
    <li>Implement proper monitoring</li>
    <li>Use API gateways</li>
    <li>Maintain service boundaries</li>
</ul>
                """,
                "tags": ["Microservices", "DevOps", "Docker"],
                "is_featured": False,
            },
            {
                "title": "Advanced React Patterns and Best Practices",
                "excerpt": "Master advanced React concepts including hooks, context, performance optimization, and modern patterns.",
                "content": """
<h2>Advanced React Development</h2>
<p>Take your React skills to the next level with advanced patterns and optimization techniques.</p>

<h3>Custom Hooks</h3>
<p>Create reusable logic with custom hooks that encapsulate stateful behavior.</p>

<h3>Context API vs State Management</h3>
<p>When to use React Context and when to reach for external state management solutions like Redux or Zustand.</p>

<h3>Performance Optimization</h3>
<ul>
    <li>React.memo for component memoization</li>
    <li>useMemo and useCallback hooks</li>
    <li>Code splitting with React.lazy</li>
    <li>Virtual scrolling for large lists</li>
</ul>

<h3>Testing Strategies</h3>
<p>Implement comprehensive testing with React Testing Library and Jest.</p>
                """,
                "tags": ["React", "JavaScript", "Performance"],
                "is_featured": True,
            },
            {
                "title": "Database Design Principles for Modern Applications",
                "excerpt": "Learn fundamental database design principles, normalization, indexing, and when to choose SQL vs NoSQL.",
                "content": """
<h2>Foundation of Data Architecture</h2>
<p>Good database design is crucial for application performance, scalability, and maintainability.</p>

<h3>Normalization Principles</h3>
<p>Understand the different normal forms and when to apply them to eliminate data redundancy.</p>

<h3>Indexing Strategies</h3>
<p>Proper indexing can dramatically improve query performance, but over-indexing can slow down writes.</p>

<h3>SQL vs NoSQL</h3>
<ul>
    <li>SQL: ACID properties, complex queries, structured data</li>
    <li>NoSQL: Scalability, flexibility, unstructured data</li>
</ul>

<h3>Performance Optimization</h3>
<ul>
    <li>Query optimization</li>
    <li>Connection pooling</li>
    <li>Caching strategies</li>
    <li>Read replicas</li>
</ul>
                """,
                "tags": ["Database Design", "PostgreSQL", "Performance"],
                "is_featured": False,
            },
            {
                "title": "Cloud-Native Development with AWS and Azure",
                "excerpt": "Build scalable applications using cloud services, serverless computing, and infrastructure as code.",
                "content": """
<h2>Embracing Cloud-Native Architecture</h2>
<p>Cloud-native development leverages cloud computing to build and run scalable applications in modern environments.</p>

<h3>Serverless Computing</h3>
<p>AWS Lambda and Azure Functions allow you to run code without managing servers.</p>

<h3>Container Services</h3>
<ul>
    <li>AWS ECS and EKS</li>
    <li>Azure Container Instances</li>
    <li>Google Cloud Run</li>
</ul>

<h3>Infrastructure as Code</h3>
<p>Use tools like Terraform, CloudFormation, or ARM templates to manage infrastructure declaratively.</p>

<h3>Monitoring and Observability</h3>
<p>Implement comprehensive monitoring with CloudWatch, Azure Monitor, or third-party solutions.</p>
                """,
                "tags": ["Cloud Computing", "AWS", "DevOps"],
                "is_featured": False,
            },
            {
                "title": "Modern JavaScript: ES2024 Features and Beyond",
                "excerpt": "Explore the latest JavaScript features and how they improve developer experience and application performance.",
                "content": """
<h2>JavaScript Evolution</h2>
<p>JavaScript continues to evolve with new features that make development more efficient and enjoyable.</p>

<h3>Latest ES2024 Features</h3>
<ul>
    <li>Array grouping methods</li>
    <li>Promise.withResolvers()</li>
    <li>String.prototype.isWellFormed()</li>
    <li>Atomics.waitAsync()</li>
</ul>

<h3>Async Programming</h3>
<p>Master async/await, promises, and the new async iteration patterns.</p>

<h3>Module System</h3>
<p>ES modules, dynamic imports, and module federation for microfrontends.</p>

<h3>Performance Considerations</h3>
<p>Optimize JavaScript performance with proper memory management and efficient algorithms.</p>
                """,
                "tags": ["JavaScript", "ES6+", "Performance"],
                "is_featured": True,
            },
            {
                "title": "Test-Driven Development: Best Practices and Tools",
                "excerpt": "Master TDD methodology with practical examples using Jest, Pytest, and other modern testing frameworks.",
                "content": """
<h2>Test-Driven Development Fundamentals</h2>
<p>TDD is a development approach where tests are written before the actual code, leading to better design and fewer bugs.</p>

<h3>The TDD Cycle</h3>
<ol>
    <li>Write a failing test (Red)</li>
    <li>Write minimal code to pass (Green)</li>
    <li>Refactor the code (Refactor)</li>
</ol>

<h3>Testing Pyramid</h3>
<ul>
    <li>Unit tests: Fast, isolated, numerous</li>
    <li>Integration tests: Medium speed, moderate isolation</li>
    <li>E2E tests: Slow, full system, fewer</li>
</ul>

<h3>Tools and Frameworks</h3>
<ul>
    <li>Jest for JavaScript</li>
    <li>Pytest for Python</li>
    <li>RSpec for Ruby</li>
    <li>Cypress for E2E testing</li>
</ul>

<h3>Best Practices</h3>
<p>Write descriptive test names, keep tests independent, and maintain test code quality.</p>
                """,
                "tags": ["Testing", "TDD", "Quality Assurance"],
                "is_featured": False,
            },
            {
                "title": "GraphQL vs REST: Choosing the Right API Strategy",
                "excerpt": "Compare GraphQL and REST APIs, understanding when to use each approach for optimal performance and developer experience.",
                "content": """
<h2>API Design Strategies</h2>
<p>Choosing between GraphQL and REST depends on your specific use case, team expertise, and application requirements.</p>

<h3>REST API Strengths</h3>
<ul>
    <li>Simple and well-understood</li>
    <li>Great caching support</li>
    <li>Wide tooling ecosystem</li>
    <li>Stateless operations</li>
</ul>

<h3>GraphQL Advantages</h3>
<ul>
    <li>Single endpoint</li>
    <li>Client-specified data fetching</li>
    <li>Strong type system</li>
    <li>Real-time subscriptions</li>
</ul>

<h3>When to Choose What</h3>
<p>REST is great for simple CRUD operations and public APIs. GraphQL excels in complex data requirements and mobile applications.</p>

<h3>Implementation Considerations</h3>
<p>Consider team expertise, caching requirements, and performance characteristics when making your choice.</p>
                """,
                "tags": ["GraphQL", "API Development", "REST"],
                "is_featured": False,
            },
            {
                "title": "Mobile-First Design: Creating Responsive Web Experiences",
                "excerpt": "Learn mobile-first design principles and techniques for creating exceptional user experiences across all devices.",
                "content": """
<h2>Mobile-First Approach</h2>
<p>With mobile traffic exceeding desktop, designing for mobile first ensures optimal experiences across all devices.</p>

<h3>Design Principles</h3>
<ul>
    <li>Touch-friendly interfaces</li>
    <li>Readable typography</li>
    <li>Fast loading times</li>
    <li>Intuitive navigation</li>
</ul>

<h3>Responsive Breakpoints</h3>
<p>Use CSS media queries to create fluid layouts that adapt to different screen sizes.</p>

<h3>Performance Optimization</h3>
<ul>
    <li>Optimize images for different densities</li>
    <li>Minimize HTTP requests</li>
    <li>Use progressive loading</li>
    <li>Implement service workers</li>
</ul>

<h3>Testing Strategies</h3>
<p>Test on real devices and use browser dev tools to simulate various screen sizes and network conditions.</p>
                """,
                "tags": ["Mobile Development", "UI/UX Design", "Responsive Design"],
                "is_featured": True,
            },
            {
                "title": "Blockchain Development for Web Developers",
                "excerpt": "Introduction to blockchain concepts and how to build decentralized applications (dApps) using modern web technologies.",
                "content": """
<h2>Blockchain Fundamentals</h2>
<p>Blockchain technology enables decentralized applications that run on distributed networks without central authorities.</p>

<h3>Key Concepts</h3>
<ul>
    <li>Distributed ledger</li>
    <li>Smart contracts</li>
    <li>Consensus mechanisms</li>
    <li>Cryptographic hashing</li>
</ul>

<h3>Development Tools</h3>
<ul>
    <li>Web3.js for Ethereum interaction</li>
    <li>Solidity for smart contracts</li>
    <li>Truffle development framework</li>
    <li>MetaMask for wallet integration</li>
</ul>

<h3>Building dApps</h3>
<p>Create decentralized applications that interact with smart contracts and provide user-friendly interfaces.</p>

<h3>Use Cases</h3>
<p>Explore applications in finance (DeFi), gaming (NFTs), supply chain, and identity management.</p>
                """,
                "tags": ["Blockchain", "Web3", "Cryptocurrency"],
                "is_featured": False,
            },
            {
                "title": "AI-Powered Code Generation and Developer Tools",
                "excerpt": "Explore how AI tools like GitHub Copilot and ChatGPT are transforming the development workflow and boosting productivity.",
                "content": """
<h2>AI in Software Development</h2>
<p>Artificial Intelligence is revolutionizing how developers write code, debug issues, and learn new technologies.</p>

<h3>Code Generation Tools</h3>
<ul>
    <li>GitHub Copilot for code suggestions</li>
    <li>OpenAI Codex for code completion</li>
    <li>TabNine for intelligent autocomplete</li>
</ul>

<h3>AI-Assisted Debugging</h3>
<p>Use AI tools to identify bugs, suggest fixes, and explain complex error messages.</p>

<h3>Best Practices</h3>
<ul>
    <li>Review AI-generated code carefully</li>
    <li>Understand the code you're using</li>
    <li>Maintain coding standards</li>
    <li>Use AI as a learning tool</li>
</ul>

<h3>Future Implications</h3>
<p>Consider how AI tools will shape the future of software development and developer roles.</p>
                """,
                "tags": ["AI", "Developer Tools", "Productivity"],
                "is_featured": True,
            },
            {
                "title": "Web Accessibility: Building Inclusive Digital Experiences",
                "excerpt": "Learn essential accessibility principles and techniques to make your web applications usable by everyone.",
                "content": """
<h2>Accessibility Fundamentals</h2>
<p>Web accessibility ensures that websites and applications are usable by people with disabilities.</p>

<h3>WCAG Guidelines</h3>
<p>Follow the Web Content Accessibility Guidelines (WCAG) 2.1 for comprehensive accessibility coverage.</p>

<h3>Key Principles</h3>
<ul>
    <li>Perceivable: Information must be presentable in ways users can perceive</li>
    <li>Operable: Interface components must be operable</li>
    <li>Understandable: Information and operation must be understandable</li>
    <li>Robust: Content must be robust enough for various assistive technologies</li>
</ul>

<h3>Implementation Techniques</h3>
<ul>
    <li>Semantic HTML markup</li>
    <li>Proper heading structure</li>
    <li>Alt text for images</li>
    <li>Keyboard navigation support</li>
    <li>Color contrast compliance</li>
</ul>

<h3>Testing Tools</h3>
<p>Use tools like axe-core, WAVE, and screen readers to test accessibility compliance.</p>
                """,
                "tags": ["Accessibility", "Inclusive Design", "UX"],
                "is_featured": False,
            },
            {
                "title": "Web Performance Optimization: Core Web Vitals and Beyond",
                "excerpt": "Master web performance optimization techniques to improve user experience and search engine rankings.",
                "content": """
<h2>Performance Matters</h2>
<p>Web performance directly impacts user experience, conversion rates, and search engine rankings.</p>

<h3>Core Web Vitals</h3>
<ul>
    <li>Largest Contentful Paint (LCP): Loading performance</li>
    <li>First Input Delay (FID): Interactivity</li>
    <li>Cumulative Layout Shift (CLS): Visual stability</li>
</ul>

<h3>Optimization Strategies</h3>
<ul>
    <li>Image optimization and modern formats</li>
    <li>Code splitting and lazy loading</li>
    <li>CDN implementation</li>
    <li>Caching strategies</li>
    <li>Minification and compression</li>
</ul>

<h3>Monitoring Tools</h3>
<p>Use Lighthouse, PageSpeed Insights, and Real User Monitoring to track performance metrics.</p>

<h3>Performance Budget</h3>
<p>Establish performance budgets to maintain fast loading times as your application grows.</p>
                """,
                "tags": ["Performance", "Web Vitals", "Optimization"],
                "is_featured": True,
            },
            {
                "title": "DevOps Culture: Bridging Development and Operations",
                "excerpt": "Understand DevOps principles, tools, and practices for efficient software delivery and team collaboration.",
                "content": """
<h2>DevOps Philosophy</h2>
<p>DevOps is a cultural shift that emphasizes collaboration between development and operations teams.</p>

<h3>Key Principles</h3>
<ul>
    <li>Collaboration and communication</li>
    <li>Automation and tooling</li>
    <li>Continuous improvement</li>
    <li>Shared responsibility</li>
</ul>

<h3>CI/CD Pipelines</h3>
<p>Implement continuous integration and deployment for faster, more reliable software delivery.</p>

<h3>Infrastructure as Code</h3>
<p>Manage infrastructure using code for version control, repeatability, and automation.</p>

<h3>Monitoring and Observability</h3>
<ul>
    <li>Application monitoring</li>
    <li>Log aggregation</li>
    <li>Distributed tracing</li>
    <li>Alerting systems</li>
</ul>
                """,
                "tags": ["DevOps", "CI/CD", "Automation"],
                "is_featured": False,
            },
            {
                "title": "The Future of Web Development: Trends and Technologies",
                "excerpt": "Explore emerging technologies and trends that will shape the future of web development in the coming years.",
                "content": """
<h2>Looking Ahead</h2>
<p>Web development continues to evolve rapidly with new technologies and paradigms emerging regularly.</p>

<h3>Emerging Technologies</h3>
<ul>
    <li>WebAssembly for near-native performance</li>
    <li>Edge computing and edge functions</li>
    <li>JAMstack architecture</li>
    <li>Micro-frontends</li>
</ul>

<h3>Development Trends</h3>
<ul>
    <li>Low-code/no-code platforms</li>
    <li>Headless CMS solutions</li>
    <li>API-first development</li>
    <li>Serverless architecture</li>
</ul>

<h3>User Experience Evolution</h3>
<p>Voice interfaces, AR/VR experiences, and ambient computing will change how users interact with web applications.</p>

<h3>Preparing for the Future</h3>
<p>Stay current with technologies, focus on fundamentals, and maintain a learning mindset.</p>
                """,
                "tags": ["Future Tech", "Web Trends", "Innovation"],
                "is_featured": True,
            },
            {
                "title": "Building Real-Time Applications with WebSockets",
                "excerpt": "Learn how to implement real-time features in your web applications using WebSockets and modern real-time frameworks.",
                "content": """
<h2>Real-Time Web Applications</h2>
<p>Real-time functionality enables instant communication between clients and servers, creating dynamic user experiences.</p>

<h3>WebSocket Fundamentals</h3>
<p>WebSockets provide full-duplex communication channels over a single TCP connection.</p>

<h3>Use Cases</h3>
<ul>
    <li>Chat applications and messaging</li>
    <li>Live collaboration tools</li>
    <li>Real-time gaming</li>
    <li>Live data dashboards</li>
    <li>Financial trading platforms</li>
</ul>

<h3>Implementation Technologies</h3>
<ul>
    <li>Socket.IO for Node.js</li>
    <li>Django Channels for Python</li>
    <li>ActionCable for Rails</li>
    <li>Native WebSocket API</li>
</ul>

<h3>Scalability Considerations</h3>
<p>Handle connection scaling, message queuing, and horizontal scaling for large real-time applications.</p>
                """,
                "tags": ["WebSockets", "Real-time", "JavaScript"],
                "is_featured": False,
            },
        ]

        # Create blog posts
        for i, post_data in enumerate(posts_data):
            # Create blog post
            publish_date = timezone.now() - timedelta(days=random.randint(1, 90))
            
            post, created = BlogPost.objects.get_or_create(
                title=post_data["title"],
                defaults={
                    "excerpt": post_data["excerpt"],
                    "content": post_data["content"],
                    "author": admin_user,
                    "status": "published",
                    "is_featured": post_data["is_featured"],
                    "publish_date": publish_date,
                    "meta_description": post_data["excerpt"][:255],
                    "read_time": random.randint(3, 12),
                    "views": random.randint(50, 500),
                },
            )

            if created:
                # Add tags
                for tag_name in post_data["tags"]:
                    try:
                        tag = BlogTag.objects.get(name=tag_name)
                        post.tags.add(tag)
                    except BlogTag.DoesNotExist:
                        self.stdout.write(f"Tag '{tag_name}' not found, skipping...")

                self.stdout.write(f"Created blog post: {post.title}")
            else:
                self.stdout.write(f"Blog post already exists: {post.title}")

        self.stdout.write(self.style.SUCCESS("Successfully added 20 more blog posts!"))
