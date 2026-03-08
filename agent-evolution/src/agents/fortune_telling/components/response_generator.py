class ResponseGenerator:
    def generate_response(self, analysis):
        # 生成自然、流畅的回应
        response = f"您好！根据您的信息，我为您进行了详细的命理分析：\n\n"
        response += f"【性格分析】\n{analysis['personality']}\n\n"
        response += f"【运势分析】\n{analysis['fortune']}\n\n"
        response += f"【问题解答】\n{analysis['specific']}\n\n"
        response += f"【分析依据】\n{analysis['reasoning']}\n\n"
        response += "希望我的分析对您有所帮助。您还有其他问题吗？"
        return response