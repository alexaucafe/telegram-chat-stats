from chat import Chat
from text import Text
from plotter import Plotter

def main():
    reverse = False

    # Getting stats
    group = Chat()
    group_stats = group.get_group_stats(reverse = reverse)

    # Getting text and saving as txt and png
    text = Text(group_stats)
    txt = text.txt
    png = text.png(font_size=60)

    with open("result.txt", "w", encoding = "utf-8") as file:
        file.write(txt)
        file.close()
        print(txt)

    png.save("result1.png")

    # Plotting and saving as png
    plotter = Plotter(group_stats)

    plt, fig = plotter.plot_members(reverse = reverse)
    fig.savefig("figure1.png", bbox_inches='tight', dpi=300)
    plt, fig = plotter.plot_days()
    fig.savefig("figure2.png", bbox_inches='tight', dpi=300)

main()