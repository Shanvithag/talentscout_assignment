# talentscout_assignment
This is a chatbot powered by open ai and streamlit, that collects candidate information including name, related tech stack etc and generates questions related.

# install the required dependecies
Python 3.11.7
Streamlit, version 1.41.1
and make sure you have installled compatible versions of openai, pymysql.

# I have used XAMMP server, mysql, for handling the data. 
# steps to create the database
1. install the xammpp server.
2. turn on apache, and mysql.
3. go to any browser and paste the link http://localhost/phpmyadmin.
4. now, create a database called talentscout.
5. create a table candidates with schema prescribed in database_schema.sql

# now for running the streamlit, openai application
1.open the anaconda powershell prompt, navigate to the environment and folder in which app.py is located
2. run the command streamlit run app.py (name with which you have saved talentscout.py)

# done!!!
