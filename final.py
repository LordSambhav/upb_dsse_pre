import re
from pydriller import Repository

def analyze_camel_issues():
    repo_url = "https://github.com/apache/camel"
    issue_ids = ["CAMEL-180", "CAMEL-321", "CAMEL-1818", "CAMEL-3214", "CAMEL-18065"]
    
    relevant_commits = []
    unique_files = set()
    total_dmm_score = 0.0

    print("Scanning repository...")
    
    issue_patterns = [re.compile(rf"\b{issue_id}\b") for issue_id in issue_ids]
    
    for commit in Repository(repo_url).traverse_commits():
        
        if any(pattern.search(commit.msg) for pattern in issue_patterns):
            relevant_commits.append(commit)
            
            for modified_file in commit.modified_files:
                if modified_file.change_type.name in ['ADD', 'MODIFY', 'DELETE']:
                    file_path = modified_file.new_path if modified_file.new_path else modified_file.old_path
                    if file_path:
                        unique_files.add(file_path)
            
            dmm_size = commit.dmm_unit_size or 0.0
            dmm_complexity = commit.dmm_unit_complexity or 0.0
            dmm_interfacing = commit.dmm_unit_interfacing or 0.0
            
            commit_avg_dmm = (dmm_size + dmm_complexity + dmm_interfacing) / 3.0
            total_dmm_score += commit_avg_dmm

    #Final calculation
    total_commits = len(relevant_commits)
    
    if total_commits == 0:
        print("No commits found matching the provided Issue IDs.")
        return

    avg_unique_files = len(unique_files) / total_commits
    avg_dmm_metrics = total_dmm_score / total_commits

    print("\n--- Results ---")
    print(f"Total relevant commits found: {total_commits}")
    print(f"Total unique files modified: {len(unique_files)}")
    print(f"1. Average unique files changed per commit: {avg_unique_files:.4f}")
    print(f"2. Average DMM metric score: {avg_dmm_metrics:.4f}")

if __name__ == "__main__":
    analyze_camel_issues()