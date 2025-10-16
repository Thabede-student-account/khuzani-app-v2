import os
from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash, session, send_from_directory
from .models import db, Page, Event, Product, Media, ContactMessage, Admin
from .forms import ContactForm, LoginForm, PageForm, EventForm, ProductForm, MediaForm
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main_bp.route('/lang/<lang_code>')
def set_language(lang_code):
    if lang_code not in current_app.config.get('BABEL_SUPPORTED_LOCALES', ['zu','en']):
        lang_code = current_app.config.get('BABEL_DEFAULT_LOCALE','zu')
    session['lang'] = lang_code
    return redirect(request.referrer or url_for('main.home'))

@main_bp.route('/')
def home():
    lang = session.get('lang', current_app.config.get('BABEL_DEFAULT_LOCALE','zu'))
    events = Event.query.order_by(Event.date.asc()).limit(3).all()
    products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    gallery = Media.query.order_by(Media.uploaded_at.desc()).limit(6).all()
    return render_template('home.html', lang=lang, events=events, products=products, gallery=gallery)

@main_bp.route('/about')
def about():
    lang = session.get('lang', current_app.config.get('BABEL_DEFAULT_LOCALE','zu'))
    page = Page.query.filter_by(slug='about').first()
    return render_template('about.html', page=page, lang=lang)

@main_bp.route('/music')
def music():
    lang = session.get('lang', current_app.config.get('BABEL_DEFAULT_LOCALE','zu'))
    page = Page.query.filter_by(slug='music').first()
    return render_template('music.html', page=page, lang=lang)

@main_bp.route('/events')
def events():
    lang = session.get('lang', current_app.config.get('BABEL_DEFAULT_LOCALE','zu'))
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template('events.html', events=events, lang=lang)

@main_bp.route('/events/<int:event_id>')
def event_detail(event_id):
    lang = session.get('lang', current_app.config.get('BABEL_DEFAULT_LOCALE','zu'))
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event, lang=lang)

@main_bp.route('/gallery')
def gallery():
    lang = session.get('lang', current_app.config.get('BABEL_DEFAULT_LOCALE','zu'))
    items = Media.query.order_by(Media.uploaded_at.desc()).all()
    return render_template('gallery.html', items=items, lang=lang)

@main_bp.route('/store')
def store():
    lang = session.get('lang', current_app.config.get('BABEL_DEFAULT_LOCALE','zu'))
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('store.html', products=products, lang=lang)

@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    lang = session.get('lang', current_app.config.get('BABEL_DEFAULT_LOCALE','zu'))
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product, lang=lang)

@main_bp.route('/contact', methods=['GET','POST'])
def contact():
    lang = session.get('lang', current_app.config.get('BABEL_DEFAULT_LOCALE','zu'))
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Umlayezo uthunyelwe — siyabonga' if lang=='zu' else 'Message sent — thank you', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form, lang=lang)

@main_bp.route('/admin/login', methods=['GET','POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('main.admin_dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('admin/login.html', form=form)

@main_bp.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('main.admin_login'))

@main_bp.route('/admin')
@login_required
def admin_dashboard():
    pages = Page.query.all()
    events = Event.query.order_by(Event.date.desc()).all()
    products = Product.query.order_by(Product.created_at.desc()).all()
    media = Media.query.order_by(Media.uploaded_at.desc()).all()
    return render_template('admin/dashboard.html', pages=pages, events=events, products=products, media=media)

@main_bp.route('/admin/pages/new', methods=['GET','POST'])
@login_required
def new_page():
    form = PageForm()
    if form.validate_on_submit():
        p = Page(
            slug=form.slug.data,
            title_zu=form.title_zu.data,
            title_en=form.title_en.data,
            content_zu=form.content_zu.data,
            content_en=form.content_en.data
        )
        db.session.add(p); db.session.commit()
        flash('Page created', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('admin/edit_page.html', form=form)

@main_bp.route('/admin/pages/edit/<int:page_id>', methods=['GET','POST'])
@login_required
def edit_page(page_id):
    p = Page.query.get_or_404(page_id)
    form = PageForm(obj=p)
    if form.validate_on_submit():
        p.slug=form.slug.data
        p.title_zu=form.title_zu.data
        p.title_en=form.title_en.data
        p.content_zu=form.content_zu.data
        p.content_en=form.content_en.data
        db.session.commit()
        flash('Page updated', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('admin/edit_page.html', form=form, page=p)

@main_bp.route('/admin/events/new', methods=['GET','POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        e = Event(
            title_zu=form.title_zu.data, title_en=form.title_en.data,
            description_zu=form.description_zu.data, description_en=form.description_en.data,
            venue=form.venue.data, date=form.date.data, ticket_link=form.ticket_link.data
        )
        db.session.add(e); db.session.commit()
        flash('Event created', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('admin/edit_event.html', form=form)

@main_bp.route('/admin/events/edit/<int:event_id>', methods=['GET','POST'])
@login_required
def edit_event(event_id):
    e = Event.query.get_or_404(event_id)
    form = EventForm(obj=e)
    if form.validate_on_submit():
        e.title_zu=form.title_zu.data; e.title_en=form.title_en.data
        e.description_zu=form.description_zu.data; e.description_en=form.description_en.data
        e.venue=form.venue.data; e.date=form.date.data; e.ticket_link=form.ticket_link.data
        db.session.commit()
        flash('Event updated','success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('admin/edit_event.html', form=form, event=e)

@main_bp.route('/admin/products/new', methods=['GET','POST'])
@login_required
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_name = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            image_name = f"{timestamp}_{filename}"
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_name)
            form.image.data.save(path)
        prod = Product(
            name_zu=form.name_zu.data, name_en=form.name_en.data,
            description_zu=form.description_zu.data, description_en=form.description_en.data,
            price=form.price.data, image=image_name
        )
        db.session.add(prod); db.session.commit()
        flash('Product added','success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('admin/edit_product.html', form=form)

@main_bp.route('/admin/products/edit/<int:product_id>', methods=['GET','POST'])
@login_required
def edit_product(product_id):
    p = Product.query.get_or_404(product_id)
    form = ProductForm(obj=p)
    if form.validate_on_submit():
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            image_name = f"{timestamp}_{filename}"
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_name))
            p.image = image_name
        p.name_zu=form.name_zu.data; p.name_en=form.name_en.data
        p.description_zu=form.description_zu.data; p.description_en=form.description_en.data
        p.price=form.price.data
        db.session.commit()
        flash('Product updated','success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('admin/edit_product.html', form=form, product=p)

@main_bp.route('/admin/media/upload', methods=['GET','POST'])
@login_required
def media_upload():
    form = MediaForm()
    if form.validate_on_submit() and form.file.data:
        filename = secure_filename(form.file.data.filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        name = f"{timestamp}_{filename}"
        form.file.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], name))
        media_type = 'video' if name.lower().endswith(('mp4','webm')) else 'image'
        m = Media(filename=name, caption_zu=form.caption_zu.data, caption_en=form.caption_en.data, media_type=media_type)
        db.session.add(m); db.session.commit()
        flash('Media uploaded','success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('admin/media_upload.html', form=form)
