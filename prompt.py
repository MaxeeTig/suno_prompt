# =============================================================================
# PYDANTIC MODELS FOR STRUCTURED OUTPUT
# =============================================================================

class SunoParameters(BaseModel):
    """Section 1: Extracted musical parameters from user input"""
    suno_title: str = Field(..., description="Creative song title that captures the essence of the story and mood")
    story_text: str = Field(..., description="Story or main plot of the song")
    tempo: str = Field(default="", description="Tempo/BPM (e.g., '165 BPM', '120 BPM')")
    genre: str = Field(default="", description="Music genre (e.g., 'glam rock', 'synthwave', 'pop')")
    mood_emotion: str = Field(default="", description="Mood and emotion (e.g., 'uplifting', 'inspiring', 'romantic')")
    vocals: str = Field(default="", description="Vocal characteristics (e.g., 'female vocal', 'male lead vocal')")
    vocals_gender: str = Field (default="", description = "Vocal gender specified by user or identified by LLM")
    instruments: str = Field(default="", description="Instrumentation (e.g., 'synthesizers', 'drums', 'violins')")
    song_structure: str = Field(default="", description="Song structure (e.g., 'Verse -> Chorus -> Verse -> Chorus -> Bridge -> Chorus')")
    lyric_style: str = Field(default="", description="Lyric style (e.g., 'contemporary pop style', 'poetic')")
    language: str = Field(default="", description="Language (e.g., 'English', 'Spanish')")


class SunoLyrics(BaseModel):
    """Section 2: Complete song lyrics with structure tags"""
    lyrics: str = Field(..., description="Complete song lyrics with structure tags")


class SunoTechnical(BaseModel):
    """Section 3: Structured technical parameters for Suno AI generation"""
    style: str = Field(..., description="Musical style and vibe description (e.g., 'Uplifting Italo Disco vibe with Synthwave influences')")
    bpm: str = Field(..., description="Beats per minute tempo (e.g., '165', '80')")
    vocals: str = Field(..., description="Vocal specifications (e.g., 'Clear female lead vocal', 'Male vocal with emotional delivery')")
    vocals_gender: str = Field(..., description="Vocal gender: 'f' for female or 'm' for male vocals")
    instrumentation: str = Field(..., description="Instrumentation and arrangement details (e.g., 'Modern pop arrangement with emphasis on synthesizers and rhythm')")


class SunoPromptResponse(BaseModel):
    """Combined output model containing all three sections"""
    suno_version: str = Field(..., description="Suno version used for generation")
    suno_parameters: SunoParameters
    suno_lyrics: SunoLyrics
    suno_technical: SunoTechnical


# =============================================================================
# SYSTEM PROMPT
# =============================================================================

SYSTEM_PROMPT = """You are an expert music producer and songwriter specializing in creating structured prompts for AI music generation.

Your task is to analyze a user's song description and generate three structured sections:

1. SUNO_PARAMETERS: Extract and structure musical parameters from the user's description
2. SUNO_LYRICS: Write complete, original song lyrics with proper structure tags
3. SUNO_TECHNICAL: Create a technical prompt optimized for Suno AI music generation

IMPORTANT GUIDELINES:
- Extract parameters by intelligently interpreting user input - users may not use technical terms but you should guess/extract the underlying parameters
- Always extract the story_text (main plot/theme) from the user's description - this is required
- Always generate a creative suno_title that captures the essence of the story and mood - this is required
- For language: By default, generate lyrics in the same language as the user's prompt. If user explicitly requests a different language (e.g., "English cover of Russian song"), use the specified language
- Leave other parameters empty ("") if not specified - do not use default values
- Write lyrics that match the extracted mood, genre, and theme
- Use proper structure tags: [Intro], [Verse 1], [Verse 2], [Chorus], [Bridge], [Outro]
- For suno_technical section: Use extracted parameters, make intelligent guesses, and enhance with creative ideas to better reflect the user's story in the target music
- Focus on style, vocals, instrumentation, and composition details
- Use "vibe" instead of "in the style of" for style descriptions
- CRITICAL: Use only plain text - NO emojis, symbols, or special characters in any output
- All text must be clean, professional, and suitable for API integration
- IMPORTANT: Keep technical descriptions concise and under 50 characters each for web UI compatibility

Example user input: "inspiring song about diving the deep sea to find love, glam rock, synthwave, 165 bpm, female vocal, uplifting"

IMPORTANT: Respond ONLY with valid JSON in this exact format. Use ONLY plain text - no emojis, symbols, or special characters:
{
  "suno_version": "v4_5",
  "suno_parameters": {
    "suno_title": "creative song title that captures the essence of the story and mood",
    "story_text": "main story/theme extracted from user input",
    "tempo": "extracted tempo or empty string",
    "genre": "extracted genre or empty string",
    "mood_emotion": "extracted mood or empty string",
    "vocals": "extracted vocal info or empty string",
    "instruments": "extracted instruments or empty string",
    "song_structure": "extracted structure or empty string",
    "lyric_style": "extracted style or empty string",
    "language": "detected or specified language"
  },
  "suno_lyrics": {
    "lyrics": "complete lyrics with [Intro], [Verse 1], [Chorus], etc. tags - PLAIN TEXT ONLY"
  },
  "suno_technical": {
    "style": "musical style and vibe description based on extracted parameters and story - PLAIN TEXT ONLY",
    "bpm": "tempo in beats per minute",
    "vocals": "detailed vocal specifications - PLAIN TEXT ONLY",
    "vocals_gender": "f or m",
    "instrumentation": "instrumentation and arrangement details - PLAIN TEXT ONLY"
  }
}"""

