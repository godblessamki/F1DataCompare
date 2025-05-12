# f1_ui.py
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from f1_backend import get_driver_stat, get_completed_2025_races, AVAILABLE_STATS

NEON_BLUE = "#00f0ff"
NEON_RED = "#ff004f"
NEON_PURPLE = "#9a00ff"
BG_DARK = "#0a0a0a"
FONT_FAMILY = "Segoe UI"

class F1Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("F1 Dashboard")
        self.geometry("1024x800")
        self.configure(bg=BG_DARK)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # === HEADER ===
        self.label = ctk.CTkLabel(
            self, text="F1 Stat Viewer",
            font=(FONT_FAMILY, 32, "bold"),
            text_color=NEON_BLUE
        )
        self.label.pack(pady=20)

        # === RACE SELECTION ===
        self.known_races = ["Bahrain", "Saudi Arabia", "Australia", "Japan", "China", "Miami"]
        self.selected_gp = ctk.StringVar(value=self.known_races[0])
        self.gp_menu = ctk.CTkOptionMenu(
            self, values=self.known_races, variable=self.selected_gp,
            fg_color=NEON_BLUE, text_color="black", button_color=NEON_PURPLE,
            font=(FONT_FAMILY, 14)
        )
        self.gp_menu.pack(pady=10)

        self.refresh_button = ctk.CTkButton(
            self, text="Refresh Race List",
            command=self.refresh_race_list,
            fg_color=NEON_RED, hover_color=NEON_PURPLE,
            font=(FONT_FAMILY, 13, "bold")
        )
        self.refresh_button.pack(pady=5)

        # === DRIVER SELECTION ===
        self.selected_driver = ctk.StringVar(value="VER")
        self.driver_menu = ctk.CTkOptionMenu(
            self, values=["VER", "LEC"], variable=self.selected_driver,
            fg_color=NEON_BLUE, text_color="black", button_color=NEON_PURPLE,
            font=(FONT_FAMILY, 14)
        )
        self.driver_menu.pack(pady=10)

        # === COMPARISON MODE ===
        self.compare_mode = ctk.BooleanVar(value=False)
        self.compare_checkbox = ctk.CTkCheckBox(
            self, text="Enable Comparison",
            variable=self.compare_mode, command=self.toggle_compare_menu,
            font=(FONT_FAMILY, 13), text_color=NEON_BLUE
        )
        self.compare_checkbox.pack(pady=5)

        self.selected_driver2 = ctk.StringVar(value="LEC")
        self.driver_menu2 = ctk.CTkOptionMenu(
            self, values=["VER", "LEC"], variable=self.selected_driver2,
            fg_color=NEON_BLUE, text_color="black", button_color=NEON_PURPLE,
            font=(FONT_FAMILY, 14)
        )
        self.driver_menu2.pack(pady=5)
        self.driver_menu2.pack_forget()

        # === STAT TYPE ===
        self.selected_stat = ctk.StringVar(value="Lap Time")
        self.stat_menu = ctk.CTkOptionMenu(
            self, values=AVAILABLE_STATS, variable=self.selected_stat,
            fg_color=NEON_BLUE, text_color="black", button_color=NEON_PURPLE,
            font=(FONT_FAMILY, 14)
        )
        self.stat_menu.pack(pady=10)

        self.plot_button = ctk.CTkButton(
            self, text="Plot Stat", command=self.load_data,
            fg_color=NEON_BLUE, hover_color=NEON_PURPLE,
            font=(FONT_FAMILY, 15, "bold")
        )
        self.plot_button.pack(pady=10)

        # === CHART FRAME ===
        self.chart_frame = ctk.CTkFrame(self, fg_color="#121212")
        self.chart_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # === LOADING BAR ===
        self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal", mode="determinate", width=300)
        self.progress_bar.set(0)
        self.progress_bar.place_forget()

    def toggle_compare_menu(self):
        if self.compare_mode.get():
            self.driver_menu2.pack(pady=5)
        else:
            self.driver_menu2.pack_forget()

    def refresh_race_list(self):
        new_races = get_completed_2025_races()
        if new_races:
            self.gp_menu.configure(values=new_races)
            self.selected_gp.set(new_races[0])

    def load_data(self):
        self.progress_bar.set(0)
        self.progress_bar.place(relx=0.5, rely=0.95, anchor="center")
        self.update_idletasks()

        gp = self.selected_gp.get()
        stat = self.selected_stat.get()
        driver1 = self.selected_driver.get()

        self.progress_bar.set(0.3)
        self.update_idletasks()

        laps1, data1, title1 = get_driver_stat(2025, gp, driver1, stat)

        laps2, data2, title2 = [], [], ""
        driver2 = None
        if self.compare_mode.get():
            driver2 = self.selected_driver2.get()
            laps2, data2, title2 = get_driver_stat(2025, gp, driver2, stat)

        self.progress_bar.set(0.7)
        self.update_idletasks()

        self.display_chart((laps1, data1, driver1), (laps2, data2, driver2), stat, gp)

        self.progress_bar.set(1.0)
        self.after(500, lambda: self.progress_bar.place_forget())

    def display_chart(self, dataset1, dataset2, stat, grand_prix):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        laps1, data1, label1 = dataset1
        laps2, data2, label2 = dataset2

        fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG_DARK)
        ax.set_facecolor(BG_DARK)

        if stat == "Tyre Compound":
            compound_colors = {
                "SOFT": "#ff2e2e",
                "MEDIUM": "#ffeb3b",
                "HARD": "#ffffff",
                "INTERMEDIATE": "#39ff14",
                "WET": "#0066ff",
                "UNKNOWN": "#aaaaaa"
            }

            colors1 = [compound_colors.get(comp.upper(), "#aaaaaa") for comp in data1]
            ax.scatter(laps1, [1] * len(data1), c=colors1, s=100, edgecolors="black", label=label1)

            if label2:
                colors2 = [compound_colors.get(comp.upper(), "#aaaaaa") for comp in data2]
                ax.scatter(laps2, [1.1] * len(data2), c=colors2, s=100, edgecolors="white", label=label2)

            for i, comp in enumerate(data1):
                ax.text(laps1[i], 1.05, comp[:3], ha="center", fontsize=8, rotation=45, color="white")

            if label2:
                for i, comp in enumerate(data2):
                    ax.text(laps2[i], 1.15, comp[:3], ha="center", fontsize=8, rotation=45, color="white")

            ax.set_yticks([])
            ax.set_ylim(0.9, 1.3)
        else:
            ax.plot(laps1, data1, marker='o', label=label1, color=NEON_BLUE)
            if label2:
                ax.plot(laps2, data2, marker='x', label=label2, color=NEON_PURPLE)
            ax.set_ylabel(stat, color="white")

        ax.set_xlabel("Lap", color="white")
        ax.set_title(f"{grand_prix} GP – {stat}", color="white")
        ax.legend()
        ax.grid(True, color="#333333")
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = F1Dashboard()
    app.mainloop()
