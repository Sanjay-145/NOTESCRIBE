def blog():
    import streamlit as st 
    from langchain.llms import OpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
    import os
    import json
    from streamlit_lottie import st_lottie

    from dotenv import load_dotenv
    load_dotenv()

    # Models
    llm= OpenAI(temperature=0.9,model_name="gpt-3.5-turbo")


    # Prompt Template
    blog_prompt_template = PromptTemplate(
        input_variables = ['product_description'],
        template = 'Write a blog post on {product_description}'
    )

    # Chain
    blog_chain = LLMChain(llm=llm, prompt=blog_prompt_template, 
                        verbose=True,
                        output_key='blog')

    # Run
    # product_description = 'best eco-friendly coffee'
    # print(blog_chain.run(product_description))

    # Prompt 2
    youtube_script_template = PromptTemplate(
        input_variables=['blog'],
        template = '''Write an engaging Youtube short video script
        for a new product based on this blog content: {blog}'''
    )

    # Chain 2
    youtube_script_chain = LLMChain(llm=llm, prompt=youtube_script_template,
                                    verbose=True,
                                    output_key='yt_script')

    # Sequential Chain
    simple_chain = SimpleSequentialChain(chains=[blog_chain,youtube_script_chain],
                                        verbose=True)
    # Run
    # product_description = 'best eco-friendly coffee'
    # print(simple_chain.run(product_description))

    # Prompt 3
    youtube_visuals_template = PromptTemplate(
        input_variables=['yt_script','blog'],
        template='''You're an amazing director, generate the scene by scene
        Description for the Youtube video based on the following script: {yt_script}
        Here is additional blog content if additional context is needed: {blog}'''
    )

    # Chain 3
    youtube_visuals_chain = LLMChain(llm=llm, prompt=youtube_visuals_template,
                                    verbose=True,
                                    output_key='yt_visuals')

    # Sequential Chain
    marketing_automation_chain = SequentialChain(
        chains=[blog_chain, youtube_script_chain, youtube_visuals_chain],
        input_variables=['product_description'],
        output_variables=['blog','yt_script','yt_visuals'],
        verbose=True
    )

    # Run
    # product_description = 'best eco-friendly coffee'
    # marketing_automation_chain(product_description)

    # Streamlit App Front End Magic!
    st.title('✨🤖 Blog generation and youtube scripting')

    #Animation
    # Load Lottie animation
    def load_lottiefile1(filepath:str):
        with open(filepath,"r") as f:
            return json.load(f)
            
    lottie_blog = load_lottiefile1("D:\\Projects\\pdf3\\templates\\blog_anim.json")

    # Display Lottie animation (logo) 
    st.markdown(
        """
        <style>
        .logo-container {
            position: absolute;
            top: 10px;
            right: 10px;
            width: 100px; /* Adjust the width as needed */
            height: 100px; /* Adjust the height as needed */
        }
        </style>
        """
    , unsafe_allow_html=True)

    # Add a container div with the logo-container class
    st.markdown("<div class='logo-container'></div>", unsafe_allow_html=True)
        
    # Display the Lottie animation inside the container
    st_lottie(lottie_blog, quality="high", width=100, height=100)


    #content
    st.text(
    """Features:
        1) Blog post
        2) Youtube script
        3) Youtube visual description
    Future: Instagram, Twitter, LinkedIn post generator""")
    user_input = st.text_input('Insert product description:',
                            placeholder='New recommended feature launch for photos app on phone.')

    if st.button('Generate') and user_input:
        app_data = marketing_automation_chain(user_input)
    
        st.divider()

        st.write(f"Generated content based on {app_data['product_description']}")

        st.write('## Blog Post')
        st.write(app_data['blog'])

        st.divider()

        st.write('## Youtube')
        st.write('### Script')
        st.write(app_data['yt_script'])
        st.write('### Visuals')
        st.write(app_data['yt_visuals'])