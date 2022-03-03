from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from ..forms import AddEvent
from ..models import Events 

calendar = Blueprint('calendar', __name__)

@calendar.route('/calendar')
@login_required
def cal():
    """[Allow to generate the template of cal.html on calendar path, if user is authenticated else return on login]
    Returns:
        [str]: [the calender page returns the events saved to the calender]
    """
    event_attributes = ['event', 'start date', 'end date', 'url']
    
    # apres bdd envents ok :events = Events.find_by_user_id(current_user.id)
    return render_template('calendar.html', events=Events.find_by_user_id(current_user.id))


@calendar.route('/add', methods=['GET', "POST"])
@login_required
def add():
    form = AddEvent()
    if form.validate_on_submit():
        Events(user_id=current_user.id, event_title=form.event_title.data, start_date=form.start_date.data, end_date=form.end_date.data,
               url=form.url.data).save_to_db()
        flash('Nouvel événement ajouté.', category='success')
        return redirect(url_for('calendar.cal'))
    return render_template('add_event.html', form=form)