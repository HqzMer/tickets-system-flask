from flask import Blueprint,redirect,url_for,render_template
from models import Ticket,db
from forms import TicketForm
from flask_login import login_required

ticketsRouting=Blueprint('ticketsRouting',__name__)

@ticketsRouting.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    form = TicketForm()
    if form.validate_on_submit():
        new_ticket = Ticket(title=form.title.data, description=form.description.data)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('ticketsRouting.tickets'))
    
    all_tickets = Ticket.query.all()
    return render_template('tickets.html', form=form, tickets=all_tickets)

@ticketsRouting.route('/ticket/<int:id>')
@login_required
def ticket_detail(id):
    ticket = Ticket.query.get_or_404(id)
    return render_template('ticket_detail.html', ticket=ticket)