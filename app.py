# app.py
import streamlit as st
import re
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database import init_db, save_user, save_results, get_all_results
from questions import QUESTIONS

def create_quadrant_plot(analytical_score, communication_score):
    """Create enhanced quadrant plot with dynamic subtitle and modern design"""
    # Determine the profile type
    if analytical_score >= 0.5 and communication_score >= 0.5:
        profile = "Strategic Communicator"
        color = "#4CAF50"  # Green
        symbol = "star"
    elif analytical_score >= 0.5 and communication_score < 0.5:
        profile = "Technical Expert"
        color = "#2196F3"  # Blue
        symbol = "diamond"
    elif analytical_score < 0.5 and communication_score >= 0.5:
        profile = "Storyteller"
        color = "#FF9800"  # Orange
        symbol = "circle"
    else:
        profile = "Intuitive Analyst"
        color = "#9C27B0"  # Purple
        symbol = "square"

    # Create figure
    fig = go.Figure()

    # Add gradient background for quadrants (subtle)
    fig.add_trace(go.Scatter(
        x=[0, 5, 5, 0],
        y=[0, 0, 5, 5],
        fill='toself',
        fillcolor='rgba(156, 39, 176, 0.1)',  # Purple tint
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=[5, 10, 10, 5],
        y=[0, 0, 5, 5],
        fill='toself',
        fillcolor='rgba(33, 150, 243, 0.1)',  # Blue tint
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=[0, 5, 5, 0],
        y=[5, 5, 10, 10],
        fill='toself',
        fillcolor='rgba(255, 152, 0, 0.1)',  # Orange tint
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=[5, 10, 10, 5],
        y=[5, 5, 10, 10],
        fill='toself',
        fillcolor='rgba(76, 175, 80, 0.1)',  # Green tint
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Add user's position with pulsing animation
    fig.add_trace(go.Scatter(
        x=[analytical_score * 10],
        y=[communication_score * 10],
        mode='markers',
        marker=dict(
            size=20,
            color=color,
            symbol=symbol,
            line=dict(
                color='white',
                width=2
            )
        ),
        name="Your Position",
        hovertemplate="<b>Your Profile</b><br>" +
                     "Analytical: %{x:.1f}/10<br>" +
                     "Communication: %{y:.1f}/10<br>" +
                     f"Type: {profile}<extra></extra>"
    ))

    # Add quadrant lines
    fig.add_hline(y=5, line_dash="dash", line_color="rgba(128, 128, 128, 0.3)", line_width=1)
    fig.add_vline(x=5, line_dash="dash", line_color="rgba(128, 128, 128, 0.3)", line_width=1)

    # Update layout
    fig.update_layout(
        title={
            'text': f"<b>Your Data Analysis Style</b><br><span style='font-size: 16px; color: {color}'>You are a {profile}</span>",
            'y':0.95,
            'x':0,
            'xanchor': 'left',
            'yanchor': 'top'
        },
        xaxis_title="Analytical Approach",
        yaxis_title="Communication Style",
        xaxis=dict(
            range=[-0.5, 10.5],
            showgrid=False,
            zeroline=False,
            ticks="outside",
            tickvals=[0, 5, 10],
            ticktext=["Beginner", "Intermediate", "Expert"]
        ),
        yaxis=dict(
            range=[-0.5, 10.5],
            showgrid=False,
            zeroline=False,
            ticks="outside",
            tickvals=[0, 5, 10],
            ticktext=["Beginner", "Intermediate", "Expert"]
        ),
        plot_bgcolor='white',
        width=800,
        height=500,
        margin=dict(t=100),
        showlegend=False
    )

    # Add quadrant labels with modern styling
    annotations = [
        dict(x=7.5, y=7.5, text="Strategic<br>Communicator", 
             font=dict(size=12, color="#4CAF50")),
        dict(x=7.5, y=2.5, text="Technical<br>Expert", 
             font=dict(size=12, color="#2196F3")),
        dict(x=2.5, y=7.5, text="Storyteller", 
             font=dict(size=12, color="#FF9800")),
        dict(x=2.5, y=2.5, text="Intuitive<br>Analyst", 
             font=dict(size=12, color="#9C27B0"))
    ]

    for annot in annotations:
        fig.add_annotation(
            x=annot["x"],
            y=annot["y"],
            text=annot["text"],
            showarrow=False,
            font=annot["font"],
            align="center",
            bordercolor=annot["font"]["color"],
            borderwidth=1,
            borderpad=4,
            bgcolor="rgba(255, 255, 255, 0.8)",
            opacity=0.8
        )

    return fig

def is_valid_email(email):
    """
    Validate email format using regex.
    Basic checks for:
    - Has @ symbol
    - Has valid domain
    - No special characters except .-_
    - Proper length
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    
    # Additional checks
    if len(email) > 254:  # Maximum length check
        return False
    
    if '..' in email:  # No consecutive dots
        return False
    
    return True
def main():
    # Initialize database
    init_db()
    
    st.set_page_config(
        page_title="Data Analysis Style Assessment",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stTitle {
            font-size: 2.5rem;
            margin-bottom: 2rem;
        }
        .profile-box {
            padding: 1.5rem;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin: 1rem 0;
        }
        .description {
            font-size: 1.1rem;
            line-height: 1.6;
        }
        </style>
        """, unsafe_allow_html=True)
    
    if 'stage' not in st.session_state:
        st.session_state.stage = 'register'
        st.session_state.answers = []
        st.session_state.user_id = None

    if st.session_state.stage == 'register':
        st.title("Data Analysis Skill Assessment (Sample)")
        
        with st.form("registration"):
            email = st.text_input("Email")
            profession = st.selectbox(
                "Current Profession",
                ["Data Analyst", "Data Scientist", "Business Analyst", "Student", "Other"]
            )
            st.markdown("*Your email will only be used to track your assessment results and further communications.*")
            
            submitted = st.form_submit_button("Start Assessment")
            
            if submitted:
                if not email or not profession:
                    st.error("Please fill in all fields")
                elif not is_valid_email(email):
                    st.error("Please enter a valid email address")
                elif email.endswith(('.test', '.example', '.invalid', '.localhost')):
                    st.error("Please use a valid email domain")
                else:
                    # Additional checks for common disposable email domains
                    disposable_domains = {'temp-mail.org', 'tempmail.com', 'throwawaymail.com'}
                    email_domain = email.split('@')[1]
                    if email_domain in disposable_domains:
                        st.error("Please use a valid business or personal email")
                    else:
                        user_id = save_user(email, profession)
                        if user_id:
                            st.session_state.user_id = user_id
                            st.session_state.stage = 'assessment'
                            st.rerun()
                        else:
                            st.error("There was an error starting your assessment. Please try again.")
                            
    elif st.session_state.stage == 'assessment':
        current_q = len(st.session_state.answers)
        if current_q < len(QUESTIONS):
            question = QUESTIONS[current_q]
            
            # Progress bar with percentage
            progress = (current_q) / len(QUESTIONS)
            st.progress(progress)
            st.write(f"Question {current_q + 1} of {len(QUESTIONS)} ({int(progress * 100)}% complete)")
            
            st.markdown(f"### {question['text']}")
            
            # Create columns for better button layout
            col1, col2 = st.columns(2)
            for i, option in enumerate(question["options"]):
                if i % 2 == 0:
                    if col1.button(option["text"], key=option["text"], use_container_width=True):
                        st.session_state.answers.append({
                            "analytical": option["analytical"],
                            "communication": option["communication"]
                        })
                        if len(st.session_state.answers) == len(QUESTIONS):
                            st.session_state.stage = 'results'
                        st.rerun()
                else:
                    if col2.button(option["text"], key=option["text"], use_container_width=True):
                        st.session_state.answers.append({
                            "analytical": option["analytical"],
                            "communication": option["communication"]
                        })
                        if len(st.session_state.answers) == len(QUESTIONS):
                            st.session_state.stage = 'results'
                        st.rerun()

    elif st.session_state.stage == 'results':
        analytical_score = sum(a["analytical"] for a in st.session_state.answers) / len(QUESTIONS)
        communication_score = sum(a["communication"] for a in st.session_state.answers) / len(QUESTIONS)
        
        save_results(
            st.session_state.user_id,
            analytical_score,
            communication_score
        )
        
        st.title("Your Sample Assessment Results")
        
        # Display the plot
        fig = create_quadrant_plot(analytical_score, communication_score)
        st.plotly_chart(fig, use_container_width=True)
        
        # Profile Box with Strengths and Opportunities
        st.markdown('<div class="profile-box">', unsafe_allow_html=True)
        
        # Determine profile and display detailed information
        if analytical_score >= 0.5 and communication_score >= 0.5:
            st.markdown("### You are a Strategic Communicator!")
            
            st.markdown("#### 💪 Key Strengths:")
            st.markdown("""
            - Balancing deep analytical insights with clear communication
            - Adapting technical content for different audiences
            - Driving data-informed decision making
            - Building bridges between technical and non-technical teams
            """)
            
            st.markdown("#### 🎯 Opportunity Areas:")
            st.markdown("""
            - Consider diving even deeper into advanced statistical methods
            - Develop frameworks to scale your communication approaches
            - Mentor others in balancing technical and communication skills
            - Lead cross-functional data initiatives
            """)

        elif analytical_score >= 0.5 and communication_score < 0.5:
            st.markdown("### You are a Technical Expert!")
            
            st.markdown("#### 💪 Key Strengths:")
            st.markdown("""
            - Deep technical expertise and thorough analysis
            - Strong attention to statistical validity
            - Excellence in research and methodology
            - Mastery of advanced analytical techniques
            """)
            
            st.markdown("#### 🎯 Opportunity Areas:")
            st.markdown("""
            - Develop skills in translating technical concepts for non-technical audiences
            - Practice creating executive summaries of your analyses
            - Incorporate more visualizations in your work
            - Focus on stakeholder engagement and relationship building
            """)

        elif analytical_score < 0.5 and communication_score >= 0.5:
            st.markdown("### You are a Storyteller!")
            
            st.markdown("#### 💪 Key Strengths:")
            st.markdown("""
            - Translating complex insights into compelling narratives
            - Creating impactful data visualizations
            - Understanding audience needs
            - Driving actionable insights from data
            """)
            
            st.markdown("#### 🎯 Opportunity Areas:")
            st.markdown("""
            - Deepen your understanding of statistical methodologies
            - Develop more robust validation techniques for your analyses
            - Build expertise in advanced analytical tools
            - Strengthen your technical documentation skills
            """)

        else:
            st.markdown("### You are an Intuitive Analyst!")
            
            st.markdown("#### 💪 Key Strengths:")
            st.markdown("""
            - Quick pattern recognition
            - Practical problem-solving approach
            - Flexibility in analytical methods
            - Focus on business impact
            """)
            
            st.markdown("#### 🎯 Opportunity Areas:")
            st.markdown("""
            - Develop a more structured approach to analysis
            - Build expertise in specific analytical tools or methods
            - Enhance your data visualization capabilities
            - Practice formal presentation of analytical findings
            """)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Development Resources Section
        st.markdown("### 📚 Recommended Next Steps")
        st.markdown("""
        To develop in your opportunity areas, consider:
        1. Scheduling a personalized consultation to create a development plan
        2. Exploring relevant training and resources
        3. Finding a mentor who complements your style
        4. Practicing new approaches in your current role
        """)
        
        # Call to Action
        st.markdown("### 🤝 Ready to Accelerate Your Growth?")
        st.markdown("""
        Book a free consultation to:
        - Review your assessment results in detail
        - Create a personalized development plan
        - Identify specific resources and opportunities
        - Set actionable goals for your growth
        
        [📅 Schedule Your Free Consultation](https://imdataanalyst.com/contact)
        
        *Let's transform your data analysis journey with targeted development in both your strengths and opportunity areas.*
        """)
        
        if st.button("Take Another Assessment", type="primary"):
            st.session_state.stage = 'register'
            st.session_state.answers = []
            st.session_state.user_id = None
            st.rerun()

if __name__ == "__main__":
    main()