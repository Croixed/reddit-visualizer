import requests
 
from plotly.graph_objs import Bar
from plotly import offline

subreddit = 'HomeNetworking'
api_call_link = f'https://www.reddit.com/r/{subreddit}/top.json?limit=16&t=month' 
# alright this technically isn't a direct API call with using my reddit API key but it gives the same output
reddit_links, upvotes = [], []
 
def get_posts(url, links_list, metrics_list):
    """
    takes an API call url as input and converts it into two
    lists so that it can be used by plotly for visualization.
    """
 
    # make an API call and store the response
    r = requests.get(url, headers={'user-agent': 'my_script'})
    print(f"Status code: {r.status_code}")
 
    # convert json response into a python dict
    posts_dict = r.json() 
    
    # pull data from the dict and append it to the metrics and links lists
    for post in posts_dict['data']['children']:
        post_title = ' '.join(post['data']['title'].split()[:4])
        post_url = post['data']['url']
 
        # using html anchor tag to make a clickable link in the plotly visualization
        post_link = f"<a href='{post_url}'>{post_title}</a>"
    
        links_list.append(post_link)
        metrics_list.append(post['data']['score'])


def initialize_data(link_list, metrics_list):
    """
    initializes the dictionary that will hold all of the data
    for the...
    """
    data = [{
        'type': 'bar',
        'x': link_list,
        'y': metrics_list,
        'marker': {
            'color': 'rgb(60, 100, 150)',
            'line': {'width': 2, 'color': 'rgb(25, 25, 25)'}
        },
        'opacity': 0.6,
    }]
    return data
 

def generate_visual():
    """
    Generates the visual figure object.
    """
    fig = {'data': data, 'layout': my_layout}
    offline.plot(fig, filename=f"outputs/{subreddit}_chart.html")
 

def initialize_layout():
    """
    Instead of making an instance of the layout class, we build
    a dictionary with all the layout properties we want to use
    """
    my_layout = {
        'title': f'Most upvoted posts on /r/{subreddit}(last 30 days)',
        'titlefont': {'size': 28},
        'xaxis': {
            'title': 'post',
            'titlefont': {'size': 24},
            'tickfont': {'size': 14},
        },
        'yaxis': {
            'title': 'upvotes',
            'titlefont': {'size': 24},
            'tickfont': {'size': 14},
        }
    }
    return my_layout


get_posts(api_call_link, reddit_links, upvotes)

data = initialize_data(reddit_links, upvotes)
my_layout = initialize_layout()
 
generate_visual()