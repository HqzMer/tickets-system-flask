from flask import Blueprint,redirect,url_for,render_template,flash
from models import Ticket,db
from forms import TicketForm
from flask_login import login_required,current_user

ticketsRouting=Blueprint('ticketsRouting',__name__)

@ticketsRouting.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    form = TicketForm()
    if form.validate_on_submit():
        new_ticket = Ticket(title=form.title.data, description=form.description.data,user_id=current_user.id)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('ticketsRouting.tickets'))
    
    all_tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('tickets.html', form=form, tickets=all_tickets)

@ticketsRouting.route('/ticket/<int:id>')
@login_required
def ticket_detail(id):
    ticket = Ticket.query.get_or_404(id)
    return render_template('ticket_detail.html', ticket=ticket)

@ticketsRouting.route('/edit_ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    # Ensure that the creator only can edit it
    if ticket.user_id != current_user.id:
        flash('No tienes permiso para editar este ticket.', 'danger')
        return redirect(url_for('index'))

    form = TicketForm(obj=ticket) 

    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        db.session.commit()
        flash('Ticket actualizado correctamente', 'success')
        return redirect(url_for('ticketsRouting.tickets'))

    return render_template('edit_ticket.html', form=form)

@ticketsRouting.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.user_id != current_user.id:  # Check user
        flash('No tienes permiso para eliminar este ticket.', 'danger')
        return redirect(url_for('index'))

    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket eliminado correctamente', 'danger')
    return redirect(url_for('ticketsRouting.tickets'))

