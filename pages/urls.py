import secrets
from django.urls import path
from django.shortcuts import redirect
from . import views
# Sitemap
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticPageSitemap, TrainingSitemap, EventSitemap, ClubSitemap

sitemaps = {
    'static': StaticPageSitemap,
    'training': TrainingSitemap,
    'event': EventSitemap,
    'club': ClubSitemap,
}

urlpatterns = [
    path('', views.home, name='home'),
path('jp/', lambda request: redirect('home', permanent=True)),
    path('fr/', lambda request: redirect('home', permanent=True)),
    path('de/', lambda request: redirect('home', permanent=True)),
    path('es/', lambda request: redirect('home', permanent=True)),
    path('about-laughter-yoga/', views.aboutly, name='about-laughter-yoga'),
    path('about-laughter-club/', views.aboutlc, name='about-laughter-club'),
    path('ly-with-school-children/', views.schoolChildren, name='school-children'),
    path('laughter-yoga-in-business/', views.business, name='business'),
    path('laughter-yoga-with-seniors/', views.seniors, name='seniors'),
    path('laughter-yoga-for-depression/', views.depression, name='depression'),
    path('laughter-yoga-for-special-needs/', views.specialNeeds, name='special-needs'),
    path('laughter-yoga-for-cancer/', views.cancer, name='cancer'),
    path('yoga-plus-laughter-yoga/', views.yogaPlusly, name='yoga-plus-ly'),
    path('laughter-yoga-research/', views.lyResearch, name='laughter-yoga-research'),

    # Basic Learning Course
    path('online-basic-learning-course/', views.basicLearningCourse, name='basic-learning-course'),
    path('online-basic-learning-course/thank-you/', views.blcSuccess, name='blc-success'),
    path('basic-learning-course-india/', views.blcIndia, name='blc-india'),
    path('basic-learning-course-india/thank-you/', views.blcIndSuccess, name='blc-ind-success'),
    path('blcNew/', views.blcNew, name='blcNew'),
    path('clylNew/', views.clylNew, name='clylNew'),

    path('mental-health/', views.mentalHealth, name='mental-health'),

    # LY Tour
    #path('india-tour/', views.indiaTour, name='india-tour'),
    #path('free-online-yoga-training/', views.freeOnlineYogaTraining, name='free-online-yoga-training'),
    #path('jaipur-tour/', views.jaipurTour, name='jaipur-tour'),
    #path('thane-navi-mumbai-tour/', views.tnvTour, name='tnm-tour'),
    #path('thane-navi-mumbai-tour/thank-you', views.tnvTourTY, name='tnm-tour-ty'),

    path('india-tour/', lambda request: redirect('basic-learning-course', permanent=True)), #redirects
    path('free-online-yoga-training/', lambda request: redirect('basic-learning-course', permanent=True)), #redirects
    path('jaipur-tour/', lambda request: redirect('basic-learning-course', permanent=True)), #redirects
    path('thane-navi-mumbai-tour/', lambda request: redirect('basic-learning-course', permanent=True)), #redirects

    path('holidays/', views.holidays, name='holidays'),
    path('online-certified-leader-training/', lambda request: redirect('basic-learning-course', permanent=True)),
    path('skype-laughter-club/', views.skypeLaughterClub, name='skype-laughter-club'),

    # Zoom Laughter Club
    path('zoom-laughter-club/', views.zoomLaughterClub, name='zoom-laughter-club'),
    path('zoom-laughter-club/thank-you-free/', views.zlcSuccess, name='zlc-success'),
    path('zlcNew/', views.zlcNew, name='zlcNew'),

    # Laughter Blogs
    path('blogs/', views.laughterBlogsList, name='laughter-blogs'),
    path('blogs/<str:slug>/', views.laughterBlogsDetail, name='laughter-blogs-detail'),
    path('blogs/category/<str:cat_slug>', views.laughterBlogCatList, name='laughter-blogs-cat'),

    # Research Articles
    path('research-articles/', views.researchArticleList, name='general-research-articles'),
    path('research-articles/<str:slug>/', views.researchArticleDetail, name='research-article-detail'),

    path('about-laughter-yoga-training/', views.aboutTraining, name='about-training'),

    path('teacher-training-by-drk/', views.teacherTraining, name='teacher-training'),
    # path('teacher-training-by-drk/', lambda request: redirect('basic-learning-course', permanent=False)),

    path('find-ly-professionals/', views.find_lyprofs, name='find-ly-professionals'),
    path('profile/<int:pk>', views.memberdetailsview, name='members-detail'),
    path('find-registered-laughter-yoga-professionals/', views.verifiedRegisteredUsers, name='find-registered-laughter-yoga-professionals'),
    path('find-trainings-worldwide/', views.FinderTrainingView, name='find-training'),
    path('find-events-worldwide/', views.FinderEventView, name='find-event'),
    path('find-clubs-worldwide/', views.FinderClubView, name='find-club'),

    # LY 2
    path('ly2', views.ly2Landing, name='ly2'),
    path('ly2/jp/', views.ly2jpLanding, name='ly2jp'),

    path('dr-kataria-diary/', views.DiaryListView, name='diary-list'),
    path('dr-kataria-diary/<str:slug>/', views.DiaryDetailView, name='diary-detail'),
    #path('laughter-yoga-articles/', views.LYArticlesListView, name='ly-articles-list'),
    #path('laughter-yoga-articles/<str:slug>/', views.LYArticlesDetailView, name='ly-article-detail'),
    path('find-world-laughter-day/', views.FinderwldView, name='find-wld'),

    path('coming-soon/', views.comingSoon, name='coming-soon'),
    path('contact/', views.contactUs, name='contact-us'),
    path('faq/', views.faq, name='faq'),
    path('watch-videos/', views.watchVideos, name='watch-videos'),
    # Info Booklet Download
    path('download-info-booklet/' + secrets.token_urlsafe(20), views.downloadInfoBooklet, name='download-info-booklet'),

    # World Laughter Day URLs
    path('world-laughter-day/', views.aboutWld, name='world-laughter-day'),
    path('world-laughter-day/download-message-from-drk/', views.wldMessage, name='wld-message-from-drk'),
    path('world-laughter-day/download-round-logo/', views.wldRoundLogo, name='wld-round-logo'),
    path('world-laughter-day/download-blue-bg-logo/', views.wldBluebgLogo, name='wld-blue-bg-logo'),
    path('world-laughter-day/download-banner/', views.wldBanner, name='wld-banner'),

    # Spiritual Retreat
    path('spiritual-retreat/', views.spiritualRetreat, name='spiritualRetreat'),
    path('spiritual-retreat/thank-you/', views.srSuccess, name='srSuccess'),
    path('spiritual-retreat/donation/', views.srPayment, name='srPayment'),

    # World Conference
    path('world-conference/', lambda request: redirect('upcomingEvents', permanent=True)),

    # Newsletter Archive
    path('prozone-newsletter/', views.proNewsletter, name='pro-newsletter'),

    # Terms and Conditions URLs
    path('terms-and-conditions/', views.termsAndConditions, name='terms-and conditions'),
    path('privacy-policy/', views.privacyPolicy, name='privacy-policy'),

    # Laughter Quotient Form
    path('find-your-laughter-quotient/', views.laughterQuotient, name='laughterQuotient'),

    path('time-zone', views.timeZone, name='time-zone'),

    # Sitemaps
    path('sitemap', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Twilio Settings
    path('5c84d2c89a4d975aff2361cd41d356ec.html', views.twilioDomainVerification, name='twilioDomainVerification'),

    path('getInvolved/list', views.getInvolvedListView, name='getInvolvedList'), #Admin
    path('getInvolved/add', views.getInvolvedAddView, name='getInvolvedAdd'), #Admin
    path('getInvolved/edit/<int:id>', views.getInvolvedEditView, name='getInvolvedEdit'), #Admin
    path('getInvolved/delete/<int:id>', views.getInvolvedDeleteView, name='getInvolvedDelete'), #Admin

    path('diary/', views.diaryList, name='diary'),# Frontend
    path('diary/<str:slug>/', views.diarydetail, name='diary-detail'),# Frontend
    path('diary/list', views.DiaryListView, name='DiaryList'), #Admin
    path('diary/add', views.DiaryAddView, name='DiaryAdd'), #Admin
    path('diary/edit/<str:slug>', views.DiaryEditView, name='DiaryEdit'), #Admin
    path('diary/delete/<str:slug>', views.DiaryDeleteView, name='DiaryDelete'), #Admin

    path('blog/', views.blogListView, name='blog'),# Frontend
    path('blog/<str:slug>/', views.blogListView, name='blog-detail'),# Frontend
    path('blog/list', views.blogListView, name='blogList'), #Admin
    path('blog/add', views.blogAddView, name='blogAdd'), #Admin
    path('blog/edit/<str:slug>', views.blogEditView, name='blogEdit'), #Admin
    path('blog/delete/<str:slug>', views.blogDeleteView, name='blogDelete'), #Admin

    path('research-articles/', views.graList, name='general-ra'), #Frontend
    path('research-articles/<str:slug>/', views.gradetail, name='general-ra-detail'), #Frontend
    path('research-articles/list', views.graListView, name='graList'), #Admin
    path('research-articles/add', views.graAddView, name='graAdd'), #Admin
    path('research-articles/edit/<str:slug>', views.graEditView, name='graEdit'), #Admin
    path('research-articles/delete/<str:slug>', views.graDeleteView, name='graDelete'), #Admin

    # Ajax Dropdowns
    path('ajax/load-countries/', views.load_countries, name='ajax_load_countries'),
    path('ajax/load-states/', views.load_states, name='ajax_load_states'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-authors/', views.load_authors, name='ajax_load_authors'),
    path('addBlogCategory/', views.addBlogCategory, name='addBlogCategory'),
]