from django.contrib import admin
from .models import AnalyticsEvents, ProductRankingMetrics, ProductRankings, SearchHistory

admin.site.register([AnalyticsEvents, ProductRankingMetrics, ProductRankings, SearchHistory])


