# --- GENERARE RĂSPUNS ---
if audio:
    user_text = "Vreau o ofertă pentru o centrală" 
    
    try:
        # Încercăm varianta stabilă cea mai probabilă pentru SDK 1.62
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=st.session_state.system_prompt
            )
        )
        ai_response = response.text
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        st.chat_message("assistant").write(ai_response)
        autoplay_audio(ai_response)
        
    except Exception as e:
        st.error(f"Eroare AI: {e}. Încercați să reîncărcați pagina.")
