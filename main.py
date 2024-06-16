import datetime
import time
import json
from gepetto import gpt, claude, groq
from yaspin import yaspin
from md2pdf.core import md2pdf
import argparse
outline_bot = gpt.GPTModelSync()
writer_bot = claude.ClaudeModelSync()
fineTune_bot = groq.GroqModelSync()

today_string = datetime.datetime.now().strftime("%Y-%m-%d")

outline_prompt = """
You are an creative copywriter tasked with writing the outline for a blog post on the topic the user provides.
You should think about the main points that the blog post should cover, the structure of the post, and the key takeaways.
The outline should be clear, well-organized, and engaging, providing a roadmap for the full blog post.
Make sure to make the outline informative and engaging.
"""

writer_prompt = """
You are a creative copywriter tasked with writing a blog post on the topic and outline the user provides.
The target audience for the blog post is general readers who are interested in the topic.  It should be informative, engaging, and easy to read.
It should not be too long and should be well-structured with clear headings and subheadings.  It should also include any key takeaways or conclusions.
If the topic is complex, you should explain it in a way that is easy for the general reader to understand.
If the topic involves weights and measure, you should primarily use imperial US units, with a metric system conversion beside them.
You should also think about SEO and include relevant keywords in the text and section titles.
"""

finetune_prompt = """
You are a copywriter tasked with editing a blog post on the topic a user has asked for.  The user will provide
the topic and also the blog post text.  You should edit the text to make it more engaging, informative, and easy to read.
You should use an upbeat and engaging tone, and make sure the text flows well and is free of errors.
"""

best_blog_prompt = """
You are an expert copywriter tasked with selecting the best blog post from a list of variations on a given topic.
You should read through the blog posts and choose the one that is the most engaging, informative, and well-written.
The blog post should be well-structured, easy to read, and free of errors.  It should also be relevant to the topic and a general target audience.
You should also consider the SEO relevance of the blog post and choose the one that is most likely to perform well in search engine rankings.
Each blog will be xml-tagged as <blog-1>...</blog-1>, <blog-2>...</blog-2>, etc.  Please respond using JSON format as follows:

{
    "best_blog": 2,
    "reasoning": "This blog post is the most engaging and informative of the options provided.  It is well-structured and free of errors.  It is also likely to perform well in search engine rankings."
}
"""

def generate_blog_post(topic, number=1):
    with yaspin(text=f"Generating outline #{number}...") as sp:
        outline = outline_bot.chat([
            {
                "role": "system",
                "content": outline_prompt
            },
            {
                "role": "user",
                "content": f"Could you write me an outline for a blog post about : {topic}"
            }
        ])
        sp.ok("✅")
    print("Generating blog post...")
    with yaspin(text=f"Generating blog post #{number}...") as sp:
        blog_post = writer_bot.chat([
            {
                "role": "system",
                "content": writer_prompt
            },
            {
                "role": "user",
                "content": f"Could you write me a blog post about : <topic>{topic}</topic>.  I have an outline for you to follow. <outline>{outline.message}</outline>",
            }
        ])
        sp.ok("✅")
    print("Fine-tuning blog post...")
    with yaspin(text=f"Fine-tuning blog post #{number}...") as sp:
        fineTuned_blog_post = fineTune_bot.chat([
            {
                "role": "system",
                "content": finetune_prompt
            },
            {
                "role": "user",
                "content": f"Could you fine-tune this blog post about : <topic>{topic}</topic>.  I have the text for you to edit. <text>{blog_post.message}</text>",
            }
        ])
        sp.ok("✅")
    total_cost = outline.cost + blog_post.cost + fineTuned_blog_post.cost
    return fineTuned_blog_post.message, total_cost

def pick_best_blog(blogs, topic):
    user_prompt = f"I have {len(blogs)} variations of a blog post on the topic: {topic}.  Could you help me choose the best one?"
    for i, blog in enumerate(blogs):
        user_prompt += f"\n\n<blog-{i+1}>\n{blog}\n</blog-{i+1}>\n\n"
    with yaspin(text="Selecting the best blog post...") as sp:
        best_blog = writer_bot.chat([
            {
                "role": "system",
                "content": best_blog_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ])
        sp.ok("✅")
    decoded_response = json.loads(best_blog.message)
    return decoded_response, best_blog.cost

def main():
    args = argparse.ArgumentParser(description="Generate a blog post on a given topic")
    args.add_argument("--topic", type=str, default="", help="Enter the topic")
    args.add_argument("--number", type=int, default=1, help="Number of variations to generate (only one final 'best' blog post will be saved)")
    args.add_argument("--extra-context", type=str, default="", help="Extra context to provide to the model")
    args = args.parse_args()
    topic = args.topic
    if not topic:
        topic = input("Enter the topic:\n")
        if not topic:
            topic = "Using a Cosori Air Fryer to cook chicken wings, comparing 'plain', 'battered' and 'breaded' styles."
    start = time.time()
    blogs = []
    total_cost = 0
    if args.extra_context:
        topic = f"{topic}. For extra context : {args.extra_context}"
    for i in range(args.number):
        blog, cost = generate_blog_post(topic, i+1)
        blogs.append(blog)
        total_cost += cost
    if len(blogs) > 1:
        choice, cost = pick_best_blog(blogs, topic)
        best_blog = blogs[choice["best_blog"] - 1]
        reasoning = choice["reasoning"]
        total_cost += cost
    else:
        best_blog = blogs[0]
        reasoning = "Only one blog post generated"
    end = time.time()
    print(f"Total time: {end - start} seconds")
    print("Total cost : ", total_cost)
    print("Best blog post:")
    print(best_blog)
    topic = topic.replace(" ", "-")
    topic = "".join([c if c.isalnum() else "-" for c in topic])
    with open(f"{today_string}_{topic}.md", "w") as f:
        f.write(best_blog)
    print(best_blog)
    print("\n\nReasoning: ", reasoning)

if __name__ == "__main__":
    main()
