def chn_frequency(articles, word):
    channel_frequency = {}
    if articles:
        for article in articles:
            channel_name = article.channel_name
            channel_frequency[channel_name] = channel_frequency.get(channel_name, 0) + 1
        chn_freq_sorted = sorted(channel_frequency.items(), key=lambda x: x[1], reverse=True)
        message = word + "\n\n"
        message += "\n".join(f"{frequency} : {channel}" for channel, frequency in chn_freq_sorted)
        return message
