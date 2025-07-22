from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class SimpleAcademicAgent:
    """
    A simple AI agent designed to answer academic questions, provide study tips,
    and summarize text passages using OpenAI's language models.
    """

    def __init__(self, api_key: str):
        """
        Initializes the agent with an OpenAI API key.

        Args:
            api_key (str): Your OpenAI API key.
        """
        if not api_key or api_key == "AIzaSyCZXksC525bwsJV4QzEaXFDPuvTe7EIogQ":
            raise ValueError(
                "OpenAI API key is not set. Please replace 'YOUR_OPENAI_API_KEY' "
                "with your actual key or set the OPENAI_API_KEY environment variable."
            )
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo" 

    def _generate_response(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Internal method to generate a response from the OpenAI model.

        Args:
            prompt (str): The input prompt for the model.
            max_tokens (int): The maximum number of tokens to generate in the response.
            temperature (float): Controls the randomness of the output. Higher values mean more random.

        Returns:
            str: The generated text response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful academic assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"An error occurred while generating response: {e}"

    def answer_academic_question(self, question: str) -> str:
        """
        Answers an academic question.

        Args:
            question (str): The academic question to answer.

        Returns:
            str: The answer to the question.
        """
        prompt = f"Answer the following academic question concisely and accurately: {question}"
        return self._generate_response(prompt, max_tokens=300)

    def provide_study_tips(self, topic: str = None) -> str:
        """
        Provides general or topic-specific study tips.

        Args:
            topic (str, optional): The specific topic for which to provide study tips.
                                   If None, general study tips are provided. Defaults to None.

        Returns:
            str: A list of study tips.
        """
        if topic:
            prompt = f"Provide 5 effective study tips for learning about {topic}."
        else:
            prompt = "Provide 5 general effective study tips for students."
        return self._generate_response(prompt, max_tokens=200)

    def summarize_text(self, text: str, length: str = "briefly") -> str:
        """
        Summarizes a given text passage.

        Args:
            text (str): The text passage to summarize.
            length (str): Desired length of the summary ('briefly', 'medium', 'detailed'). Defaults to 'briefly'.

        Returns:
            str: The summarized text.
        """
        if length == "briefly":
            prompt = f"Summarize the following text in one to two sentences: {text}"
            max_tokens = 80
        elif length == "medium":
            prompt = f"Summarize the following text in a paragraph: {text}"
            max_tokens = 150
        elif length == "detailed":
            prompt = f"Provide a detailed summary of the following text: {text}"
            max_tokens = 300
        else:
            prompt = f"Summarize the following text: {text}"
            max_tokens = 100 # Default to brief if length is invalid

        return self._generate_response(prompt, max_tokens=max_tokens)

# --- Example Usage ---
if __name__ == "__main__":

    api_key = "YOUR_OPENAI_API_KEY" 

    try:
        agent = SimpleAcademicAgent(api_key=api_key)
    except ValueError as e:
        print(f"Initialization Error: {e}")
        print("Please ensure your OpenAI API key is correctly set.")
        exit()

    print("Welcome to the Simple Academic Agent!")
    print("You can ask academic questions, get study tips, or summarize text.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nHow can I help you? (e.g., 'question: What is photosynthesis?', 'tips: history', 'summarize: [text]')\n> ").strip()

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        if user_input.lower().startswith("question:"):
            question = user_input[len("question:"):].strip()
            print("\nAgent's Answer:")
            print(agent.answer_academic_question(question))
        elif user_input.lower().startswith("tips:"):
            topic = user_input[len("tips:"):].strip()
            if topic:
                print(f"\nAgent's Study Tips for {topic.capitalize()}:")
            else:
                print("\nAgent's General Study Tips:")
            print(agent.provide_study_tips(topic if topic else None))
        elif user_input.lower().startswith("summarize:"):
            text_to_summarize = user_input[len("summarize:"):].strip()
            if not text_to_summarize:
                print("Please provide text to summarize.")
                continue
            # You can extend this to ask for summary length (briefly, medium, detailed)
            print("\nAgent's Summary (brief):")
            print(agent.summarize_text(text_to_summarize, length="briefly"))
        else:
            print("Invalid command. Please use 'question:', 'tips:', or 'summarize:'.")
