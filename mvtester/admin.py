from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from mvtester.models import Goal, GoalStats, Treatment, Experiment

class GoalStatsGoalInline(admin.TabularInline):
    model = GoalStats
    fk_name = 'goal'
    can_delete = False
    extra = 0
    template = 'mvtester/admin/goalstats_goal_inline.html'

class GoalAdmin(ModelAdmin):
    inlines = (GoalStatsGoalInline,)

class GoalStatsTreatmentInline(admin.TabularInline):
    model = GoalStats
    can_delete = False
    fk_name = 'treatment'
    extra = 0
    template = 'mvtester/admin/goalstats_treatment_inline.html'

class TreatmentAdmin(ModelAdmin):
    inlines = (GoalStatsTreatmentInline,)

class TreatmentInline(admin.TabularInline):
    model = Treatment
    fk = 'experiment'
    
class ExperimentAdmin(admin.ModelAdmin):
    inlines = (TreatmentInline,)
    list_display = ('name','slug','current_winners')
    
    def current_winners(self,obj):
        winners = []
        for goal in Goal.objects.filter(experiment=obj):
            winner = obj.get_winner(goal.slug)
            if winner:
                winners.append(winner.name)
        return ','.join(winners)

    
admin.site.register(Experiment,ExperimentAdmin)
admin.site.register(Treatment,TreatmentAdmin)
admin.site.register(Goal,GoalAdmin)
