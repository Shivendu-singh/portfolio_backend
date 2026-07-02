from django.core.management.base import BaseCommand

from api.models import Achievement, Education, Experience, Profile, Project, Skill


class Command(BaseCommand):
    help = "Seed portfolio database with Shivendu Kumar resume content"

    def handle(self, *args, **options):
        Profile.objects.all().delete()
        Education.objects.all().delete()
        Skill.objects.all().delete()
        Project.objects.all().delete()
        Experience.objects.all().delete()
        Achievement.objects.all().delete()

        Profile.objects.create(
            name="Shivendu Kumar",
            tagline="Ceramic Engineering @ IIT BHU · Full-Stack · CP Specialist",
            phone="7667684727",
            email="shivendusingh98351@gmail.com",
            github_url="https://github.com/Shivendu-singh",
            linkedin_url="https://linkedin.com/in/shivendu-kumar",
            location="Varanasi, UP · India",
            bio=(
                "B.Tech Ceramic Engineering student at IIT (BHU) Varanasi with a passion for "
                "full-stack development, neuromorphic computing, and competitive programming. "
                "I build high-performance systems that bridge material science and software engineering."
            ),
            resume_url="",
        )

        Education.objects.create(
            institution="Indian Institute of Technology (BHU) Varanasi",
            degree="Bachelor of Technology in Ceramic Engineering",
            location="Varanasi, UP",
            start_year=2024,
            end_year=2028,
            gpa_label="Current CPI",
            gpa_value="8.67",
            highlights=[],
            order=1,
        )
        Education.objects.create(
            institution="Loyola Convent School",
            degree="Class XII (CBSE) · Class X (CBSE)",
            location="Ranchi, Jharkhand",
            start_year=2022,
            end_year=2024,
            gpa_label="Class XII / Class X",
            gpa_value="94.6% / 96.6%",
            highlights=[],
            order=2,
        )

        skills_data = [
            ("C++", "LANG", "code"),
            ("Python", "LANG", "code"),
            ("JavaScript", "LANG", "code"),
            ("C", "LANG", "code"),
            ("SQL", "LANG", "database"),
            ("HTML/CSS", "LANG", "layout"),
            ("React.js", "FRAME", "react"),
            ("Node.js", "FRAME", "server"),
            ("Django", "FRAME", "django"),
            ("FastAPI", "FRAME", "zap"),
            ("PyTorch", "FRAME", "brain"),
            ("NumPy", "FRAME", "grid"),
            ("Pandas", "FRAME", "table"),
            ("Scikit-learn", "FRAME", "chart"),
            ("Git/GitHub", "TOOL", "git"),
            ("Docker", "TOOL", "container"),
            ("LaTeX", "TOOL", "file"),
            ("Data Structures & Algorithms", "COURSE", "binary"),
            ("Object Oriented Programming", "COURSE", "box"),
            ("DBMS", "COURSE", "database"),
            ("Operating Systems", "COURSE", "cpu"),
        ]
        skill_map = {}
        for idx, (name, category, icon) in enumerate(skills_data):
            skill_map[name] = Skill.objects.create(
                name=name, category=category, icon_key=icon, order=idx
            )

        igzo = Project.objects.create(
            title="Neuromorphic Computing: IGZO Memristor Model",
            subtitle="Python, PyTorch, ML",
            date_range="Jan. 2026 – Present",
            description="Physics-aware deep learning model for IGZO memristor dynamics and spiking neural networks.",
            highlights=[
                "Engineered a physics-aware Deep Learning model to simulate IGZO memristor dynamics, optimizing conductance modulation for 99% energy efficiency compared to CMOS-based equivalents.",
                "Simulated Spiking Neural Networks (SNNs) with biologically plausible LTP/LTD synaptic plasticity, achieving state-of-the-art accuracy on MNIST dataset for edge-computing scenarios.",
                "Bridged material physics and AI to enable in-memory computing architectures, reducing von Neumann bottleneck latency.",
            ],
            github_url="https://github.com/Shivendu-singh",
            live_url="",
            is_research=True,
            order=1,
        )
        igzo.technologies.set([
            skill_map["Python"], skill_map["PyTorch"], skill_map["NumPy"], skill_map["Pandas"]
        ])

        hisab = Project.objects.create(
            title="HisabKitab",
            subtitle="Django, Golang, PostgreSQL, Microservices",
            date_range="Feb. 2026 – Present",
            description="Microservices-based financial platform for group expense splitting and ledger management.",
            highlights=[
                "Architected a microservices-based financial platform; decoupled Django (Auth/User Management) from a high-performance Golang transaction engine to handle heavy computational loads.",
                "Implemented recursive debt simplification algorithms (O(N) graph reduction) to minimize transaction edges and real-time WebSocket updates for group expense splitting.",
                "Designed a double-entry ledger system capable of handling 10k+ concurrent requests with sub-50ms latency using Go's Goroutines and channel orchestration.",
            ],
            github_url="https://github.com/Shivendu-singh",
            live_url="",
            is_research=False,
            order=2,
        )
        hisab.technologies.set([
            skill_map["Django"], skill_map["SQL"], skill_map["Docker"], skill_map["Git/GitHub"]
        ])

        cfbuddy = Project.objects.create(
            title="CF Buddy: AI-Powered CP Companion",
            subtitle="Django, Chart.js, GenAI",
            date_range="Dec. 2025",
            description="AI-driven dashboard for competitive programming progress and personalized learning paths.",
            highlights=[
                "Developed an AI-driven dashboard that analyzes submission history to generate personalized learning paths and targeted problem campaigns based on weak topic clusters.",
                "Integrated GenAI models to provide context-aware code reviews, time-complexity analysis, and optimization hints for failed submissions, effectively serving as a virtual coach.",
                "Visualized performance metrics for 500k+ users using Chart.js, optimizing frontend rendering with local caching to ensure 60 FPS smooth transitions.",
            ],
            github_url="https://github.com/Shivendu-singh",
            live_url="",
            is_research=False,
            order=3,
        )
        cfbuddy.technologies.set([
            skill_map["Django"], skill_map["JavaScript"], skill_map["React.js"]
        ])

        Experience.objects.create(
            organization="Technex'26 (IIT BHU Tech Fest)",
            role="Marketing Executive",
            location="Varanasi, UP",
            start_label="2025",
            end_label="2026",
            bullets=[
                "Led corporate outreach and sponsorship negotiations, securing key partnerships for a 50k+ footfall event.",
                "Managed a team of 20+ volunteers for on-ground marketing and campus-wide promotional activities.",
            ],
            order=1,
        )
        Experience.objects.create(
            organization="Technex'25 (IIT BHU Tech Fest)",
            role="Branding Coordinator",
            location="Varanasi, UP",
            start_label="2024",
            end_label="2025",
            bullets=[
                "Revamped digital identity, resulting in a 35% increase in social media engagement and brand visibility.",
            ],
            order=2,
        )

        Achievement.objects.create(
            platform="codeforces",
            handle="Shivendu-singh",
            profile_url="https://codeforces.com/profile/Shivendu-singh",
            max_rating=1495,
            current_rating=1495,
            rank_text="Specialist",
            problems_solved=500,
            extra_stats={"global_rank_div3": 1361, "note": "Max rating 1495"},
            order=1,
        )
        Achievement.objects.create(
            platform="codechef",
            handle="shivendu_singh",
            profile_url="https://www.codechef.com/users/shivendu_singh",
            max_rating=1826,
            current_rating=1826,
            rank_text="4-Star",
            problems_solved=0,
            extra_stats={"country_rank": 3530, "global_rank": 4241},
            order=2,
        )
        Achievement.objects.create(
            platform="leetcode",
            handle="Shivendu-singh",
            profile_url="https://leetcode.com/u/Shivendu-singh",
            max_rating=1959,
            current_rating=1959,
            rank_text="Contest Rating 1959",
            problems_solved=200,
            extra_stats={"focus": "Graphs, DP, Trees"},
            order=3,
        )

        self.stdout.write(self.style.SUCCESS("Resume data seeded successfully."))
