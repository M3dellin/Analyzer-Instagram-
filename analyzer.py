from instaloader import Instaloader, Profile
from datetime import datetime
import pandas as pd
import os

class InstagramAnalyzer:
    def __init__(self):
        self.loader = Instaloader()
        
    def login(self, username, password):
        """
        Faz login no Instagram (opcional, mas recomendado para evitar limitações)
        """
        try:
            self.loader.login(username, password)
            print("Login realizado com sucesso!")
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
    
    def analyze_profile(self, username):
        """
        Analisa um perfil do Instagram e retorna suas informações
        """
        try:
            profile = Profile.from_username(self.loader.context, username)
            
            # Coletando dados básicos do perfil
            profile_data = {
                "username": profile.username,
                "nome_completo": profile.full_name,
                "biografia": profile.biography,
                "website": profile.external_url,
                "seguidores": profile.followers,
                "seguindo": profile.followees,
                "num_posts": profile.mediacount,
                "privado": profile.is_private,
                "verificado": profile.is_verified,
                "data_analise": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Se o perfil não for privado, coletar dados dos posts
            if not profile.is_private:
                posts_data = []
                for post in profile.get_posts():
                    post_info = {
                        "data_post": post.date_local.strftime("%Y-%m-%d %H:%M:%S"),
                        "likes": post.likes,
                        "comentarios": post.comments,
                        "legenda": post.caption if post.caption else "",
                        "localizacao": post.location if post.location else "",
                        "hashtags": post.hashtags,
                        "mencoes": post.tagged_users,
                        "url": f"https://www.instagram.com/p/{post.shortcode}/"
                    }
                    posts_data.append(post_info)
                
                # Criar DataFrame com dados dos posts
                df_posts = pd.DataFrame(posts_data)
                
                # Análises adicionais dos posts
                profile_data.update({
                    "media_likes": df_posts["likes"].mean(),
                    "media_comentarios": df_posts["comentarios"].mean(),
                    "total_hashtags": sum(len(tags) for tags in df_posts["hashtags"]),
                    "total_mencoes": sum(len(mentions) for mentions in df_posts["mencoes"])
                })
                
                # Salvar dados em arquivos
                self.save_data(username, profile_data, df_posts)
                
            return profile_data
            
        except Exception as e:
            print(f"Erro ao analisar perfil: {e}")
            return None
    
    def save_data(self, username, profile_data, posts_df=None):
        """
        Salva os dados coletados em arquivos CSV
        """
        # Criar pasta para os dados se não existir
        os.makedirs("instagram_data", exist_ok=True)
        
        # Salvar dados do perfil
        pd.DataFrame([profile_data]).to_csv(
            f"instagram_data/{username}_profile.csv", 
            index=False
        )
        
        # Salvar dados dos posts se disponíveis
        if posts_df is not None:
            posts_df.to_csv(
                f"instagram_data/{username}_posts.csv", 
                index=False
            )

# Exemplo de uso
if __name__ == "__main__":
    analyzer = InstagramAnalyzer()
    
    # Opcional: fazer login para evitar limitações
    # analyzer.login("seu_usuario", "sua_senha")
    
    # Analisar perfil
    perfil = "instagram"  # exemplo com perfil oficial do Instagram
    dados = analyzer.analyze_profile(perfil)
    
    if dados:
        print("\nDados coletados com sucesso!")
        print("\nInformações básicas do perfil:")
        for key, value in dados.items():
            print(f"{key}: {value}")