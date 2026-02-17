def generate_insights(records):
    if not records:
        return ["No data available"]

    insights = []

    avg_ctr = sum(r.ctr for r in records) / len(records)
    avg_cpc = sum(r.cpc for r in records) / len(records)
    avg_cpa = sum(r.cpa for r in records) / len(records)

    if avg_ctr < 0.02:
        insights.append("Overall CTR is below industry benchmark (2%). Improve creatives or targeting.")

    if avg_cpc > 20:
        insights.append("CPC is high. Consider optimizing audience segmentation.")

    if avg_cpa > 50:
        insights.append("Cost per acquisition is high. Optimize conversion funnel.")

    if not insights:
        insights.append("Campaign performance is stable and within healthy ranges.")

    return insights
