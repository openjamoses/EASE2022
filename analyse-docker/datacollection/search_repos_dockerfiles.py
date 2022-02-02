import csv
import pandas as pd

import csv
import pandas as pd
import math

from datacollection.utils.GIT import get_data


def main():
    path = '/Volumes/Cisco/Summer2022/Docker/Dataset/repos/'

    data_file = open(path + 'ml_docker_repositories2.csv', mode='w', newline='',
                                  encoding='utf-8')
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['Repos','ML_Related', 'topic', 'commits', 'contributors', 'issues','pulls', 'releases','repo_size','stars','forks','open_issues','archived','created_at', 'updated_at','docker_files_count', 'file_names', 'file_paths','language','homepage', 'description'])

    data_df = pd.read_csv(path + 'TestingMLmodels.csv')
    Repos = data_df.Repos.values.tolist()
    ML_Related = data_df.ML_Related.values.tolist()
    topic = data_df.topic.values.tolist()
    commits = data_df.commits.values.tolist()
    contributors = data_df.contributors.values.tolist()
    issues = data_df.issues.values.tolist()
    pulls = data_df.pulls.values.tolist()
    releases = data_df.releases.values.tolist()
    repo_size = data_df.repo_size.values.tolist()
    stars = data_df.stars.values.tolist()
    forks = data_df.forks.values.tolist()
    open_issues = data_df.open_issues.values.tolist()
    archived = data_df.archived.values.tolist()
    created_at = data_df.created_at.values.tolist()
    updated_at = data_df.updated_at.values.tolist()
    language = data_df.language.values.tolist()
    homepage = data_df.homepage.values.tolist()
    description = data_df.description.values.tolist()

    data_df = pd.read_csv(path + 'combined/combined_initial_ml_docker_repositories.csv')
    ReposL = data_df.Repos.values.tolist()


    cm_docker_repos = 0
    ct = 0
    for index in range(len(Repos)):
        total_count = 0
        if not Repos[index] in ReposL:
            docker_flag = 0
            names_str = ''
            paths_str = ''
            url = 'https://api.github.com/search/code?q=filename:Dockerfile+repo:{}'.format(Repos[index])
            data_docker, ct = get_data(url, ct)  # GitHub(url3, ct).getResponse()
            if data_docker != None:
                total_count = data_docker['total_count']
                if total_count > 0:
                    docker_flag = 1
                    for item_obj in data_docker['items']:
                        name = item_obj['name']
                        path = item_obj['path']
                        names_str += name + '; '
                        paths_str += path + '; '

            if total_count > 0:
                cm_docker_repos += 1
                data_writer.writerow(
                    [Repos[index],ML_Related[index], topic[index], commits[index], contributors[index], issues[index], pulls[index], releases[index], repo_size[index], stars[index],
                     forks[index], open_issues[index], archived[index], created_at[index], updated_at[index], total_count, names_str,
                     paths_str, language[index], homepage[index], description[index]])
        if index%100 == 0:
            print(index, Repos[index], total_count, 'Docker repos: ', cm_docker_repos)
    data_file.close()
if __name__ == '__main__':
    main()
