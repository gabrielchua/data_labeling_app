DEFINITIONS = """
#### 1. **hateful**  
   Text that discriminates, criticizes, insults, denounces, or dehumanizes a person or group on the basis of a protected identity (e.g., race, religion, nationality, ethnicity, or other protected categories under Singapore law).

   A text can at most belong to one of the to severity levels below:

   - **1.1 discriminatory**  
 	Contains derogatory or generalized negative statements targeting a protected group.

   - **1.2 hate_speech**  
 	Explicit calls for harm or violence against a protected group; or language praising or justifying violence toward them.  

#### 2. **insults**  
   Text that demeans, humiliates, mocks, or belittles a person or group without referencing a protected trait (e.g., personal attacks on race, religion, nationality).

#### 3. **sexual**  
   Text that depicts or indicates sexual interest, activity, or arousal through direct or indirect references to sexual acts, body parts, or other adult content.

    A text can at most belong to one of the to severity levels below:

   - **3.1 content_not_appropriate_for_minors**  
 	Mild-to-moderate sexual content possibly unsuitable for individuals under 16; may include factual discussions of sex, sexuality, or sexual preferences.

   - **3.2 content_not_appropriate_for_all_ages**  
 	Sexually explicit content intended for adults, featuring graphic descriptions or otherwise inappropriate for broad audiences.  

#### 4. **physical_violence**  
   Text expressing threats, glorification, or intentions of physical harm or injury toward a person, group, or entity.

#### 5. **self_harm**  
   Text suggesting, promoting, or expressing intent to self-harm or commit suicide.

    A text can at most belong to one of the to severity levels below:

   - **5.1 self_harm_ideation**  
 	Expressions of suicidal thoughts, self-harm intent, or content encouraging self-harm.

   - **5.2 self_harm_action_or_suicide**  
 	Descriptions or indicators of ongoing or imminent self-harm behavior.  

#### 6. **all_other_misconduct**  
   Text that seeks or provides information about engaging in misconduct, wrongdoing, criminal activity, or that threatens to harm, defraud, or exploit others.

   A text can at most belong to one of the to severity levels below:

   - **6.1 not_socially_accepted**  
 	Advocates or instructs on unethical or immoral activities (not necessarily illegal but socially condemned).

   - **6.2 illegal_activites**  
 	Seeks or provides instructions to commit illegal activities or serious wrongdoing; includes credible threats of severe harm.  

""".strip()

CATEGORIES = [
    "hateful",
    "insult",
    "sexual",
    "physical_violence",
    "self_harm",
    "misconduct"
]

HATEFUL_MAPPING = {
    "NIL": "FALSE",
    "discriminatory": "level_1_discriminatory",
    "hate speech": "level_2_hate_speech"
}
INSULT_MAPPING = {
    "NIL": "FALSE", 
    "insult": "insult"
}
SEXUAL_MAPPING = {
    "NIL": "FALSE",
    "not appropriate for minors": "level_1_not_appropriate_for_minors",
    "not appropriate for all ages": "level_2_not_appropriate_for_all_ages"
}
PHYSICAL_VIOLENCE_MAPPING = {
    "NIL": "FALSE",
    "physical violence": "physical_violence"
}
SELF_HARM_MAPPING = {
    "NIL": "FALSE",
    "ideation/intent": "level_1_self_harm_intent",
    "actual self-harm/sucide": "level_2_self_harm_action"
}
MISCONDUCT_MAPPING = {
    "NIL": "FALSE",
    "generally not socially accepted": "level_1_not_socially_accepted",
    "illegal": "level_2_illegal_activities"
}
