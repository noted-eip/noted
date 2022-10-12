from user_story import UserStory
from pprint import pprint
import logging


def generate_workload_visualization(user_stories: list[UserStory]):
    user_workload_dict = dict[str, float]()

    for story in user_stories:
        if len(story.assignees) == 0:
            logging.error(f"'{story.title}' has no assignees")
            continue
        number_of_assignees = float(len(story.assignees))
        for assignee in story.assignees:
            if story.duration_in_days == 'X':
                continue
            if assignee not in user_workload_dict:
                user_workload_dict[assignee] = (
                    float(story.duration_in_days) / number_of_assignees
                )
            else:
                user_workload_dict[assignee] += (
                    float(story.duration_in_days) / number_of_assignees
                )

    pprint(user_workload_dict)
