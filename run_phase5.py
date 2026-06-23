from analytics.dashboard_metrics import get_dashboard_metrics

metrics = get_dashboard_metrics()

for key, value in metrics.items():
    print(f"{key}: {value}")