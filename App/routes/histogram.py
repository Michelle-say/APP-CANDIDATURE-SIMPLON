from flask import Blueprint, render_template
from ..models import Users, Candidacy
import plotly.express as px
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json as js
import pandas as pd

histogram = Blueprint("histogram", __name__, static_folder="../static", template_folder="../templates")

@histogram.route('/show_histogram')
def show_histogram():

        """[Allow to generate the template of statistic_hist.html to display histogram of the status of the apprenants]

    # Returns:
    #     [str]: [Show histogram page]
    # """
        # Prepare histogram of Apprenants with and witout alternance
        list_no_alternance= Users.get_list_without_alternance()
        list_with_alternance = Users.get_list_with_alternance()

        full_list_df = pd.DataFrame(columns = ['Name', 'Alternance'])

        for user_info in list_with_alternance:
            full_list_df = full_list_df.append({'Name': user_info[1]+' '+ user_info[0], 'Alternance': 'avec alternance'}, ignore_index=True)

        for user_info in list_no_alternance:
            full_list_df = full_list_df.append({'Name': user_info['first_name']+' '+ user_info['last_name'], 'Alternance': 'sans alternance'}, ignore_index=True)
        
        
        fig = px.histogram(full_list_df, x='Alternance', title = "Nombre d'apprenant en alternance", color='Alternance')
        fig.update_layout(height=400, width=600, yaxis_title="No. of Apprenants")
        plot_json1 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Prepare pie chart of Apprenants with and witout alternance
        pie_df = pd.DataFrame(columns = ['Status', 'Apprenants'])
        pie_df['Status'] = ['avec alternance', 'sans alternance']
        pie_df['Apprenants'] = [len(full_list_df.loc[full_list_df['Alternance'] =='avec alternance']), len(full_list_df.loc[full_list_df['Alternance'] =='sans alternance'])]
        

        fig = px.pie(pie_df, values='Apprenants', names='Status', title = "Pourcentage d'apprenant en alternance")
        fig.update_layout(height=500, width=500, legend_title_text='Alternance')
        plot_json2 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        kwargs = {
        'plot_json1' : plot_json1,
        'plot_json2' : plot_json2,
        }
    
        return render_template('statistic_hist.html', **kwargs)


@histogram.route('/show_histogram_entreprise')
def show_histogram_entreprise():
        """[Allow to generate the template of statistic_hist.html to display histogram of the status of the apprenants]

    # Returns:
    #     [str]: [Show histogram page]
    # """

        # user_name = Users.find_by_user_id(id)

        list_no_alternance= Users.get_list_without_alternance()
        list_with_alternance = Users.get_list_with_alternance()
        all_users_candidacy = Users.get_full_list()
        all_user_registered = Users.find_all_isUsers()

        get_full_name_list=[]

        for info in all_user_registered:
            get_full_name_list.append([info['id'], info['email_address']])


        entreprise_count_df = pd.DataFrame(columns = ['ID', 'No_Entreprise', 'No_Entreprise_str', 'Alternance'])

        list_email_no_alternance = []
        for user_info in list_no_alternance:
            list_email_no_alternance.append(user_info['email_address'])
        
        for info in get_full_name_list:
            activity = Candidacy.find_by_user_id(info[0])
            if info[1] in list_email_no_alternance:
                entreprise_count_df = entreprise_count_df.append({'ID':id, 'No_Entreprise': len(activity), 'No_Entreprise_str': str(len(activity)),'Alternance':'sans alternance'}, 
                    ignore_index=True)
            else:
                entreprise_count_df = entreprise_count_df.append({'ID':id, 'No_Entreprise': len(activity),'Alternance':'avec alternance'}, 
                    ignore_index=True)

        # Sort database
        entreprise_count_df = entreprise_count_df.sort_values(by=['No_Entreprise'])
        sequence_hist = [*range(entreprise_count_df['No_Entreprise'].max()+2)] 

        # Display histograme #1 
        fig = px.histogram(entreprise_count_df, x='No_Entreprise', title = 'Nombre de candidature par apprenant',color="No_Entreprise",
            category_orders={"No_Entreprise": sequence_hist})

        fig.update_layout(yaxis_title="No. des Apprenants", xaxis_title="No. des Candidature")
        fig.update_xaxes(type='category')       
        fig.update_layout(height=400, width=600, legend_title_text='No. Candidature')
        plot_json1 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Display pie chart #1 
        fig = px.pie(entreprise_count_df, names='No_Entreprise', title = 'Pourcentage de candidature par apprenant')

        fig.update_layout(height=500, width=500, legend_title_text='No. Candidature')
        plot_json2 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Display histograme #2
        fig = px.histogram(entreprise_count_df, x='No_Entreprise', title = 'Répartition des apprenants par nombre de candidature', 
            color="Alternance", barmode="group",
            category_orders={"No_Entreprise": sequence_hist})
    
        fig.update_layout(height=400, width=600, yaxis_title="No. of Apprenants", xaxis_title="No. des Apprenants")
        fig.update_xaxes(type='category')   
        plot_json3 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


        # Display histograme #4
        unique_list_df=pd.DataFrame(columns = ['User_ID', 'Entreprise', 'Ville', 'Contact_Full_Name', 'Contact_Email', 'Contact_Mobilephone'])
        full_list = Candidacy.get_all_in_list_entreprise()
        unique_list = []

        # 1cls.user_id ,2cls.entreprise,3cls.ville_entreprise, 4cls.contact_full_name, 5cls.contact_email, 6cls.contact_mobilephone

        for info in full_list:
            if info not in unique_list:
                unique_list.append(info)
                unique_list_df = unique_list_df.append({'User_ID': info[0], 'Entreprise':info[1], 'Ville': info[2], 
                    'Contact_Full_Name': info[3],'Contact_Email': info[4], 'Contact_Mobilephone': info[5]}, 
                    ignore_index=True)

        
        fig = px.histogram(unique_list_df, x='Ville', title = 'Répartition géographique des candidatures',color="Ville")
        #     # category_orders={"No_Entreprise": sequence_hist})

        fig.update_layout(yaxis_title="No. des Entreprise")
        fig.update_xaxes(type='category')       
        fig.update_layout(height=400, width=600)
        plot_json4 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)        

        kwargs = {
        'plot_json1' : plot_json1,
        'plot_json2' : plot_json2,
        'plot_json3' : plot_json3,
        'plot_json4' : plot_json4
        }
    
        return render_template('statistic_hist_entreprise.html', **kwargs)