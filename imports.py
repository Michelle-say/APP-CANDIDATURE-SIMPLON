from collections import UserString
from flask import render_template, redirect, url_for, flash, request
from App import db, app, mail, login_manager
from datetime import date, datetime
from .models import Users, Candidacy
from .forms import Login, AddCandidacy, ModifyCandidacy, ModifyPassword, ModifyProfile, CheckEmail, CheckPwd, AddCandidacy_verif
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
import plotly.express as px
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json as js
import pandas as pd
import random
import string
import cloudinary.uploader
import logging as lg
import csv
import difflib as dif