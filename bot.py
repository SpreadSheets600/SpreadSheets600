import discord
from discord.ext import commands
from datetime import datetime
import asyncio

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Sample note data
SAMPLE_NOTES = [
    {
        "title": "Introduction to Python Programming",
        "subject": "Computer Science",
        "date": "2024-01-15",
        "uploader": "Prof. Smith",
        "content": "Basic concepts of Python programming including variables, data types, and control structures.",
        "tags": ["python", "programming", "basics"],
        "file_size": "2.3 MB",
        "downloads": 156
    },
    {
        "title": "Calculus Derivatives and Integrals",
        "subject": "Mathematics",
        "date": "2024-01-20",
        "uploader": "Dr. Johnson",
        "content": "Comprehensive guide to calculus derivatives and integrals with examples.",
        "tags": ["calculus", "derivatives", "integrals"],
        "file_size": "4.1 MB",
        "downloads": 89
    },
    {
        "title": "World War II History Overview",
        "subject": "History",
        "date": "2024-01-25",
        "uploader": "Prof. Brown",
        "content": "Detailed analysis of World War II events, causes, and consequences.",
        "tags": ["wwii", "history", "warfare"],
        "file_size": "3.7 MB",
        "downloads": 234
    },
    {
        "title": "Organic Chemistry Reactions",
        "subject": "Chemistry",
        "date": "2024-02-01",
        "uploader": "Dr. Wilson",
        "content": "Study guide for organic chemistry reactions and mechanisms.",
        "tags": ["organic", "chemistry", "reactions"],
        "file_size": "5.2 MB",
        "downloads": 167
    },
    {
        "title": "Shakespeare's Hamlet Analysis",
        "subject": "Literature",
        "date": "2024-02-05",
        "uploader": "Prof. Davis",
        "content": "Literary analysis of Hamlet including themes, characters, and symbolism.",
        "tags": ["shakespeare", "hamlet", "literature"],
        "file_size": "1.8 MB",
        "downloads": 98
    },
    {
        "title": "Physics Quantum Mechanics",
        "subject": "Physics",
        "date": "2024-02-10",
        "uploader": "Dr. Anderson",
        "content": "Introduction to quantum mechanics principles and applications.",
        "tags": ["quantum", "physics", "mechanics"],
        "file_size": "6.1 MB",
        "downloads": 145
    },
    {
        "title": "Data Structures and Algorithms",
        "subject": "Computer Science",
        "date": "2024-02-15",
        "uploader": "Prof. Miller",
        "content": "Comprehensive guide to data structures including arrays, linked lists, trees, and graphs.",
        "tags": ["algorithms", "data-structures", "programming"],
        "file_size": "7.3 MB",
        "downloads": 289
    },
    {
        "title": "Economic Principles and Theory",
        "subject": "Economics",
        "date": "2024-02-20",
        "uploader": "Dr. Taylor",
        "content": "Basic economic principles including supply and demand, market structures.",
        "tags": ["economics", "theory", "markets"],
        "file_size": "3.9 MB",
        "downloads": 123
    },
    {
        "title": "Cell Biology and Genetics",
        "subject": "Biology",
        "date": "2024-02-25",
        "uploader": "Prof. Garcia",
        "content": "Study of cell structure, function, and genetic principles.",
        "tags": ["biology", "cells", "genetics"],
        "file_size": "4.8 MB",
        "downloads": 201
    },
    {
        "title": "French Grammar Essentials",
        "subject": "French",
        "date": "2024-03-01",
        "uploader": "Mme. Dubois",
        "content": "Essential French grammar rules and conjugations for intermediate learners.",
        "tags": ["french", "grammar", "language"],
        "file_size": "2.1 MB",
        "downloads": 87
    },
    {
        "title": "Advanced Statistics Methods",
        "subject": "Mathematics",
        "date": "2024-03-05",
        "uploader": "Dr. Chen",
        "content": "Advanced statistical methods including hypothesis testing and regression analysis.",
        "tags": ["statistics", "analysis", "hypothesis"],
        "file_size": "5.7 MB",
        "downloads": 165
    },
    {
        "title": "Environmental Science Climate Change",
        "subject": "Environmental Science",
        "date": "2024-03-10",
        "uploader": "Prof. Green",
        "content": "Comprehensive study of climate change causes, effects, and mitigation strategies.",
        "tags": ["environment", "climate", "sustainability"],
        "file_size": "8.2 MB",
        "downloads": 278
    }
]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='notes')
async def notes_index_old(ctx):
    """Original note index command - shows too much information without pagination"""
    embed = discord.Embed(
        title="📚 Study Notes Index",
        description=f"Showing all {len(SAMPLE_NOTES)} notes available:",
        color=0x3498db
    )
    
    # Show only first 10 notes (current limitation)
    notes_to_show = SAMPLE_NOTES[:10]
    
    for i, note in enumerate(notes_to_show, 1):
        # Too much information per note (current problem)
        field_value = (
            f"**Subject:** {note['subject']}\n"
            f"**Date:** {note['date']}\n"
            f"**Uploader:** {note['uploader']}\n"
            f"**Content:** {note['content']}\n"
            f"**Tags:** {', '.join(note['tags'])}\n"
            f"**File Size:** {note['file_size']}\n"
            f"**Downloads:** {note['downloads']}"
        )
        embed.add_field(
            name=f"{i}. {note['title']}", 
            value=field_value, 
            inline=False
        )
    
    if len(SAMPLE_NOTES) > 10:
        embed.set_footer(text=f"⚠️ Showing 10 of {len(SAMPLE_NOTES)} notes. No way to see more!")
    
    await ctx.send(embed=embed)

# Pagination view class for improved notes command
class NotesView(discord.ui.View):
    def __init__(self, notes, notes_per_page=7):
        super().__init__(timeout=300)
        self.notes = notes
        self.notes_per_page = notes_per_page
        self.current_page = 0
        self.total_pages = (len(notes) + notes_per_page - 1) // notes_per_page
        self.update_buttons()

    def update_buttons(self):
        # Disable/enable buttons based on current page
        self.previous_button.disabled = (self.current_page == 0)
        self.next_button.disabled = (self.current_page >= self.total_pages - 1)

    def get_current_notes(self):
        start = self.current_page * self.notes_per_page
        end = start + self.notes_per_page
        return self.notes[start:end]

    def create_embed(self):
        current_notes = self.get_current_notes()
        
        embed = discord.Embed(
            title="📚 Study Notes Index",
            description=f"Browse through available study notes",
            color=0x2ecc71
        )
        
        for i, note in enumerate(current_notes, 1):
            # Show only essential information (improved UX)
            field_value = (
                f"📖 **Subject:** {note['subject']}\n"
                f"📅 **Date:** {note['date']}\n"
                f"👤 **Uploader:** {note['uploader']}"
            )
            
            global_index = (self.current_page * self.notes_per_page) + i
            embed.add_field(
                name=f"{global_index}. {note['title']}", 
                value=field_value, 
                inline=True
            )
        
        # Add page indicator
        embed.set_footer(
            text=f"Page {self.current_page + 1} of {self.total_pages} • {len(self.notes)} total notes"
        )
        
        return embed

    @discord.ui.button(label='◀ Previous', style=discord.ButtonStyle.secondary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='▶ Next', style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='🔄 Refresh', style=discord.ButtonStyle.primary)
    async def refresh_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        # Disable all buttons when view times out
        for item in self.children:
            item.disabled = True

@bot.command(name='notes_new')
async def notes_index_new(ctx, per_page: int = 7):
    """Improved note index command with pagination"""
    if per_page < 5 or per_page > 10:
        per_page = 7  # Default to 7 if out of range
    
    view = NotesView(SAMPLE_NOTES, per_page)
    embed = view.create_embed()
    
    await ctx.send(embed=embed, view=view)

@bot.command(name='help_notes')
async def help_notes(ctx):
    """Show help for note commands"""
    embed = discord.Embed(
        title="📚 Notes Commands Help",
        description="Available commands for browsing study notes:",
        color=0xe74c3c
    )
    
    embed.add_field(
        name="!notes",
        value="Old version - shows all details without pagination",
        inline=False
    )
    
    embed.add_field(
        name="!notes_new [per_page]",
        value="New version with pagination (5-10 notes per page, default: 7)",
        inline=False
    )
    
    embed.add_field(
        name="Features of new version:",
        value="• Pagination with Previous/Next buttons\n"
              "• Shows only essential info (title, subject, date, uploader)\n"
              "• Configurable notes per page (5-10)\n"
              "• Page indicators\n"
              "• Disabled buttons at limits\n"
              "• Clean, readable design",
        inline=False
    )
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    # This is a demo bot - in production you'd use a real token
    print("Bot code created successfully!")
    print("To run the bot, you would need to:")
    print("1. Install discord.py: pip install discord.py")
    print("2. Create a Discord application and bot")
    print("3. Replace 'YOUR_BOT_TOKEN' with your actual bot token")
    print("4. Run: python bot.py")