from rapidfuzz import fuzz
from utils.normalization import normalize_name

def cluster_names(names, threshold=85):
    clusters = []

    for name in names:
        norm_name = normalize_name(name)
        added = False
        for cluster in clusters:
            rep = normalize_name(cluster[0])
            score = fuzz.partial_ratio(norm_name, rep)
            if score >= threshold:
                cluster.append(name)
                added = True
                break
        if not added:
            clusters.append([name])
    return clusters

names = ["John Smith", "J Smith", "SMITH, JOHN","Sweta Singh","S. Singh"]
clusters = cluster_names(names)
output = {
    f"entity_{i+1}": cluster
    for i, cluster in enumerate(clusters)
}
print(output) # {'entity_1': ['John Smith', 'J Smith', 'SMITH, JOHN'], 'entity_2': ['Sweta Singh', 'S. Singh']}
