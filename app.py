import redis
from flask import Flask, render_template, request, redirect
from link_shorter import LinkShorter
from logger import Logger

logger = Logger.create_logger()
app = Flask(__name__)

redis_storage_provider = redis.Redis(host='localhost', port=6379)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/short_link', methods=['POST'])
def short_link():
    try:
        link_shorter = LinkShorter(redis_storage_provider)

        source_link = request.form['link']
        result = link_shorter.save_link(source_link)

        return request.host_url + result
    except Exception as ex:
        logger.error("Incoming request to create short link %s failed with error - %s", short_link, ex)
        return render_template('error.html'), 500


@app.route('/<redirect_link>')
def redirect_short_link(redirect_link):
    if redirect_link == 'favicon.ico':
        return

    try:
        link_shorter = LinkShorter(redis_storage_provider)
        result = link_shorter.get_source_link(redirect_link)

        if result is not None:
            return redirect(result, code=302)
        else:
            logger.warning("Couldn't found any saved links by short link %s", redirect_link)
            return render_template("link_not_found.html", link=request.host_url + redirect_link)
    except BaseException as ex:
        logger.error("When trying to process redirect by short link %s an critical error occurred - %s",
                     redirect_link, ex)
        return render_template('error.html'), 500


if __name__ == '__main__':
    app.run()
