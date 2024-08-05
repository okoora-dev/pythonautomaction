import iris

iris.cls("Embedded.Utils").SetNameSpace("%SYS")
ref = iris.cls("SYS.Stats.Dashboard").Sample()
last_backup = ref.LastBackup
# check if variable is empty
if not last_backup:
    last_backup = "Never"
# content data dictionary to store data to be used in HTML page
content = {
    'ApplicationErrors': ref.ApplicationErrors,
    'CSPSessions': ref.CSPSessions,
    'CacheEfficiency': ref.CacheEfficiency,
    'DatabaseSpace': ref.DatabaseSpace,
    'DiskReads': ref.DiskReads,
    'DiskWrites': ref.DiskWrites,
    'ECPAppServer': ref.ECPAppServer,
    'ECPAppSrvRate': ref.ECPAppSrvRate,
    'ECPDataServer': ref.ECPDataServer,
    'ECPDataSrvRate': ref.ECPDataSrvRate,
    'GloRefs': ref.GloRefs,
    'GloRefsPerSec': ref.GloRefsPerSec,
    'GloSets': ref.GloSets,
    'JournalEntries': ref.JournalEntries,
    'JournalSpace': ref.JournalSpace,
    'JournalStatus': ref.JournalStatus,
    'LastBackup': last_backup,
    'LicenseCurrent': ref.LicenseCurrent,
    'LicenseCurrentPct': ref.LicenseCurrentPct,
    'LicenseHigh': ref.LicenseHigh,
    'LicenseHighPct': ref.LicenseHighPct,
    'LicenseLimit': ref.LicenseLimit,
    'LicenseType': ref.LicenseType,
    'LockTable': ref.LockTable,
    'LogicalReads': ref.LogicalReads,
    'Processes': ref.Processes,
    'RouRefs': ref.RouRefs,
    'SeriousAlerts': ref.SeriousAlerts,
    'ShadowServer': ref.ShadowServer,
    'ShadowSource': ref.ShadowSource,
    'SystemUpTime': ref.SystemUpTime,
    'WriteDaemon': ref.WriteDaemon,
    'tot_pro': tot_pro,
    'tot_msg': tot_msg,
    'tot_usr': tot_usr,
    'tot_apps': tot_apps,
    'tot_ev': tot_ev,
    'tot_ev_assert': tot_ev_assert,
    'tot_ev_error': tot_ev_error,
    'tot_ev_warning': tot_ev_warning,
    'tot_ev_info': tot_ev_info,
    'tot_ev_trace': tot_ev_trace,
    'tot_ev_alert': tot_ev_alert
}
# return content

@app.route("/")
def index():
    #get dashboard data in dictionary variable
    content = util.get_dashboard_stats()
    return render_template('index.html', content = content)
