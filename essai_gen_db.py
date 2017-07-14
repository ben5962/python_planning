# coding: utf-8
import sqlalchemy as sa
from sqlalchemy import CheckConstraint, Column, Date, DateTime, Table, Text, UniqueConstraint
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


t_VUE_heures_annu_janjan = Table(
    'VUE_heures_annu_janjan', metadata,
    Column('annee', NullType),
    Column('mois', NullType),
    Column('semaine', NullType),
    Column('heure_semaine_travaillees', NullType)
)


t_hs_dues_hebdo = Table(
    'hs_dues_hebdo', metadata,
    Column('a', NullType),
    Column('m', NullType),
    Column('s', NullType),
    Column('t', NullType),
    Column('hs_25_dues', NullType),
    Column('h50_l', NullType),
    Column('h50_i', NullType),
    Column('hs_50_dues', NullType),
    Column('eqv_t_hs_25_dues', NullType),
    Column('eqv_t_hs_50_l_dues', NullType),
    Column('eqv_t_hs_50_i_dues', NullType),
    Column('eqv_t_tot_h_dues', NullType)
)


t_old_table = Table(
    'old_table', metadata,
    Column('debut_periode', DateTime),
    Column('fin_periode', DateTime),
    Column('jour_travaille', Date),
    CheckConstraint('fin_periode > debut_periode'),
    UniqueConstraint('debut_periode', 'fin_periode', 'jour_travaille')
)


class PeriodesTravaillee(Base):
    __tablename__ = 'periodes_travaillees'
    __table_args__ = (
        CheckConstraint('fin_periode > debut_periode'),
        UniqueConstraint('debut_periode', 'fin_periode', 'jour_travaille')
    )

    debut_periode = Column(DateTime, primary_key=True, nullable=False)
    fin_periode = Column(DateTime, primary_key=True, nullable=False)
    jour_travaille = Column(Date, primary_key=True, nullable=False)


t_pff = Table(
    'pff', metadata,
    Column('mouais', Text)
)


class Planning(Base):
    __tablename__ = 'planning'

    debut_poste = Column(DateTime, primary_key=True, nullable=False, unique=True)
    fin_poste = Column(DateTime, primary_key=True, nullable=False, unique=True)
    nom_poste = Column(Text)
    categorie_poste = Column(Text)


t_plus_de_48 = Table(
    'plus_de_48', metadata,
    Column('annee', NullType),
    Column('mois', NullType),
    Column('semaine', NullType),
    Column('heure_semaine_travaillees', NullType)
)


t_vue_35_semaine = Table(
    'vue_35_semaine', metadata,
    Column('annee', NullType),
    Column('mois', NullType),
    Column('semaine', NullType),
    Column('heure_semaine_travaillees', NullType)
)


t_vue_35_semaine_hsup_sans_bonif = Table(
    'vue_35_semaine_hsup_sans_bonif', metadata,
    Column('annee', NullType),
    Column('mois', NullType),
    Column('semaine', NullType),
    Column('heure_semaine_travaillees', NullType),
    Column('heure_sup_payee_25', NullType),
    Column('heures_sup_25_effectuees_semaine', NullType),
    Column('heures_sup_50_effectuees_semaine', NullType),
    Column('heures_sup_50_ille_semaine', NullType)
)


t_vue_CP_semaine = Table(
    'vue_CP_semaine', metadata,
    Column('annee', NullType),
    Column('mois', NullType),
    Column('semaine', NullType),
    Column('heure_semaine_CP', NullType)
)


t_vue_cumul_annu_juin_a_mai = Table(
    'vue_cumul_annu_juin_a_mai', metadata,
    Column('annee_annu', NullType),
    Column('mois', NullType),
    Column('vol_annu', NullType)
)

engine = sa.create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(bind=engine)

