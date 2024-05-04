from django.urls import path
from django.urls.conf import include
from . import views
from django_email_verification import urls as email_urls

urlpatterns = [
	path('',views.home,name = "home"),
	path('register/', views.register, name="register"),
	path('login/', views.cryptLogin, name="login"),
	path('leaderboard/', views.leaderboard, name="leaderboard"),
	# path('lvl/',views.dq, name="questions"),
	path('lvl/',views.questions, name="questions"),
	path('logout/',views.logoutUser, name="logout"),
	path('rules/',views.rules, name = "rules"),
	path('alert/', views.dq, name = "dq"),
	path('af850b2e4f014ecd9f332e02388bdc96/', views.logs, name = "logs"),
	path('winner/',views.winner, name = "winner"),
	path('abcd/',views.abcd, name = "abcd"),
	path('0NBSc28A/',views.lvl16, name = "0NBSc28A"),
	path('stevejobs/',views.lvl20, name = "stevejobs"),
	path('poldercrash/',views.lvl29, name = "poldercrash"),
	path('email/',include(email_urls))
]