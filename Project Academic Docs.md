Princess Sumaya University for Technology King Hussein School for Computing Sciences

## Policy Jarl

### AuthZ/AuthN Guardrail for an AI DB Agent

## Prepared By:

## Omitted

## Supervised By:

## Omitted

Project Submitted in Partial Fulfillment of the Requirements for the Degree of Science in Cybersecurity

### Submitted: May 2026

# Declaration of Originality

This document has been written entirely by the undersigned team members of the project. The source of every quoted text is clearly cited and there is no ambiguity in where the quoted text begins and ends. The source of any illustration, image or table that is not the work of the team members is also clearly cited. We are aware that using non-original text or material or paraphrasing or modifying it without proper citation is a violation of the university’s regulations and is subject to legal actions.

Names and Signatures of team members:

Omitted

# Acknowledgements

We would like to sincerely thank everyone who has helped us along the way. We have reached this milestone thanks in large part to your support, valuable advice, and solid trust in our mission.

Before anything else, we would like to express our sincere gratitude to our devoted supervisor, Dr. Mu'awya Al-Dala'ien. His assistance, insightful advice, and direction have been crucial in helping to mold our Project and advance us towards our objectives. We would like to thank Princess Sumaya University for Technology and King Hussein School of Computing Sciences. We have a strong foundation for our academic and professional development thanks to our exceptional instructors and resources. Being a part of an organization that encourages creativity and innovation is a true honor.

We also wish to express our profound appreciation to our classmates and fellow students. Your cooperation, wisdom, and friendships have tremendously improved our experience and enabled us to overcome many obstacles.

Finally, but just as importantly, we need to sincerely thank our friends and family. Their support, love, and tolerance have been a continual source of courage, inspiring us to keep going when things get difficult. Their assistance has been a true blessing to us during this journey.

We are blessed to have such an incredible support system, and for that, we are forever grateful.


ii

# Table of Contents

Declaration of Originality ................................................................................................................i Acknowledgements .........................................................................................................................ii Table of Contents .......................................................................................................................... iii

List of Figures ................................................................................................................................. v List of Tables .................................................................................................................................vi Abbreviations ................................................................................................................................vii Abstract viii

Chapter 1 Introduction ................................................................................................................... 1 1.1 Overview ................................................................... 1 1.2 Problem Statement ................................................................... 5 1.3 Significance of the Project ................................................................... 7

1.4 Project Objectives ................................................................... 8 1.5 Project Contribution ................................................................... 9 1.6 Outline of the report ................................................................. 10 Chapter 2 Project Plan ................................................................................................................. 12

2.1 Project Deliverables ................................................................. 12 2.2 Project Tasks ................................................................. 13 2.3 Roles and Responsibilities ................................................................. 15 2.4 Risk Assessment ................................................................. 16 2.5 Cost Estimation ................................................................. 21

2.6 Project Management Tools ................................................................. 22 Chapter 3 Literature Review and Related Work .......................................................................... 23 3.1 Related Work ................................................................. 23 3.2 Knowledge Gap ................................................................. 26

3.2.1 Critical Analysis ................................................................. 26 Chapter 4 Requirements Specification ......................................................................................... 32 4.1 Stakeholders ................................................................. 32 4.2 Platform Requirements ................................................................. 33

4.3 Functional Requirements ................................................................. 35 4.4 Non-Functional Requirements ................................................................. 36 4.5 Other Requirements ................................................................. 37 Chapter 5 System Design ............................................................................................................. 38

5.1 Architectural Design ................................................................. 38 5.2 Logical Model Design ................................................................. 41 5.3 Physical Model Design ................................................................. 46 Chapter 6 Implementation............................................................................................................ 53

6.1 General Implementation Description ................................................................. 53

iii

6.2 Pipeline Implementation Description ................................................................. 56

6.3 Model Implementation ................................................................. 56 6.4 Additional Implementation Details ................................................................. 57 Chapter 7 Testing ......................................................................................................................... 60 7.1 Testing Approach ................................................................. 60

7.2 Testing Results ................................................................. 69 Chapter 8 Conclusions and Future Work ..................................................................................... 72 8.1 Conclusions ................................................................. 72 8.2 Future work ................................................................. 72

References..................................................................................................................................... 74 Appendices .................................................................................................................................... 77 ................................................................................................................................... 77 A.1 Users’ Manual ................................................................. 77

................................................................................................................................... 80 B.1 Document Changes ................................................................. 80 ................................................................................................................................... 81 C.1 Code Documentation ................................................................. 81

................................................................................................................................... 84 D.1 Ethical Document ................................................................. 84

iv

# List of Figures

Figure 2.1: A Gantt chart visualizing the project timeline in weeks. .............................. 15 Figure 5.1: An architectural graph of an agentic system without any external………....38 Figure 5.2: An architectural graph of an agentic system with a policy-driven guardrail 39 Figure 5.3: A figure showing the three layers separating the main functions ................. 40 Figure 5.4: A cross-sectional graph of the three-layered architecture. ........................... 41 Figure 5.5: An activity diagram showing the various paths............................................ 43 Figure 5.6: Sequence diagram illustrating the runtime interaction ................................. 44 Figure 5.7: A Use-Case diagram illustrating the various actors ..................................... 45 Figure 5.8: A component diagram illustrating how the various part .............................. 46 Figure 5.9: A database diagram illustrating 2 different data strictures ........................... 47

Figure 5.10: A normalized database diagram for the test use case company.................. 48 Figure 5.11: A screenshot of part of the Rego file used for the test company ................ 49 Figure 5.12: A screenshot showing how the context store would store .......................... 49 Figure 5.13: A screenshot of one of the Kibana main views called “Audit Logs” ......... 50 Figure 5.14: A screenshot of the Kibana Human in the Loop view ................................ 50 Figure 5.15: A screenshot of the Telegram chat view of the admin showing. ................ 51 Figure 5.16: A screenshot of the Kibana showing the “Waiting Room” View .............. 52 Figure 5.17: A screenshot of the Kibana showing the “Current Users” View ................ 52 Figure 5.18: A screenshot the Kibana main general dashboard ...................................... 52 Figure 6.1: A simple physical representation of the guardrail environment ................... 55 Figure 7.1: A screenshot showing the seed data that is being filled with our tables…....59 Figure 7.2: A screenshot showing the results of the automated test ............................... 59 Figure 7.3: A screenshot showing how anon users cannot speak ................................... 60 Figure 7.4: A screenshot showing how a guest users...................................................... 60 Figure 7.5: A screenshot showing the extensive help menu of the admin user .............. 61 Figure 7.6: A screenshot showing how admin user has access to all table freely ........... 61 Figure 7.7: A screenshot showing how user management access that the admin ........... 62 Figure 7.8: A screenshot showing the role switching menu for the admin ..................... 62 Figure 7.9: A screenshot showing the agent returning the full “payroll” table to admin 63 Figure 7.10: A screenshot showing both help menus available to an admin user........... 63 Figure 7.11: A screenshot showing the smaller help menu of guest users...................... 64 Figure 7.12: A screenshot showing how a HR Analyst .................................................. 64 Figure 7.13: A screenshot showing the test results of the “final_exam.py ..................... 71

v

# List of Tables

Table 2.1: A table describing required tasks ................................................................... 14 Table 2.2: A table showing each team member and their roles ...................................... 15 Table 2.3: A table assessing risks for each of the operation stages ................................ 16 Table 2.4: A table describing mitigation strategies for discovered risks ........................ 19 Table 2.5: A matrix visualizing the severity and priority of each Risk .......................... 21 Table 2.6: A table comparing the prices of the two extremes ......................................... 21 Table 3.1: Legend for the following gap matrix showing criteria and their meanings ... 28 Table 3.2: Gap matrix showing each system’s criteria evaluation.................................. 29 Table 4.1: A table showing stakeholder, their roles, and their level of importance ........ 32 Table 4.2: A matrix visualizing the severity and priority of each Risk .......................... 35

Table 7.1: A matrix showing the permission of each role and table ............................... 61 Table 7.2: A table showing our conclusions based on the automated gauntlets ............. 68

vi

Abbreviations AI Artificial Intelligence LLM Large Language Models API Application Programming Interface OPA Open Policy Agent DevOps Development Operations CI/CD Continuous Integration/ Continuous Development ISO International Organization for Standardization IEC International Electrotechnical Commission OWASP Open World-Wide Application Security Project ATLAS Adversarial Threat Landscape for Artificial-Intelligence System PaC Policy as Code HITL Human In The Loop GUI Graphical User Interface CLI Command Line Interface RBAC Role-Based Access Control PII Personal Identifiable Information

JSON JavaScript Object Notation SMART Specific, Measurable, Achievable, Relevant ReAct Reason and Act SOC Security Operation Center SaaS Software as a Service SLA Service Level Agreement AWS Amazon Web Service GPT Generative Pre-trained Transformer HTTPs Hypertext Transfer Protocol secure TLS Transport Layer Security

JWT JSON Web Token ELK Elasticsearch, Logstash, Kibana SQL Structured Query Language DLP Data Leakage Prevention

Policy Jarl


### Abstract

Over the past decade, artificial intelligence has evolved from limited generative text systems to agentic models capable of autonomous, multi-step reasoning and action. As these systems are increasingly integrated into critical workflows across industries and government, they introduce new challenges for security, governance, and regulatory compliance. Significant progress has been made in the fields of governance, cybersecurity, and AI control individually, but a standardized and reliable mechanism that bridges these fields together and enforces trust across these systems is still immature.

This project document presents Policy Jarl, a guardrail that introduces authentication and authorization to an AI agent that governs a database filled tables of different severity levels. The guardrail acts as a deterministic, extensible, and auditable protection layer that serves the functions of authentication, authorization, and role-based access control over SQL queries and natural language going in and out of the system, ensuring a zero- trust architecture where explicit policy decisions are grounded in explainable formal rules and obvious artifacts.

Globally recognized standards, regulations, and security frameworks were consulted in the design and implementation of the proposed system to ensure relevant, transparent, and repeatable enforcement that serves as a unified policy-driven control mechanism over the system-wide environment that the agentic AI operates within, with a heavy utilization of role-based-access-control.

Keywords: AI Governance; AI Security; AI Trust; AI Agent; Guardrail; Open Policy Agent (OPA); Rego; Policy-as-Code (PaC); ISO/IEC 42001; OWASP Top 10 LLM; Zero-Trust; Human-In-The-Loop (HITL); Role-Based Access Control (RBAC).

viii

## Chapter 1 Introduction

1.1 Overview

1.1.1 Scientific and Technical Background

A certain level of conceptual understanding and technical expertise is required to completely benefit from viewing the documentation. The following sub-section aims to supplement and standardize a few of the core concepts that will repeatedly be mentioned across this documentation, although it will not start from zero:

[1] What Makes an AI Agentic

Both agentic AI and generative AI are forms of advanced artificial intelligence and can be used together, as they have distinct functionalities.

Generative AI, as the name implies, is focused on the creation of new content such as text, images, code, music, and videos. It does so by using a large language model (LLM) as its "brain" that has been trained on a large amount of content that can be melded together using a set of complex "thinking" algorithms to be able to generate or alter content at the request of a prompt from a user.

Agentic AI is the subset of generative AI that is centered around the idea of automation and minimizing human interference by orchestration and execution agents that use LLMs as the "brain" to perform actions through tools and interactions with external systems. Agentic AI goes past content generation and function calling into planned multi-step tasks based on complex reasoning traces.

An AI agent is built on a set of key concepts that enable it to work autonomously and interact with its environment dynamically. These concepts or technologies are the following:

1. Perception: its ability to interact and gather information from its environment.

2. Reasoning: it uses an LLM to analyse the gathered data to understand the context, formulate solutions, and triage them.

3. Planning: The AI uses the information it analysed to develop a course of action. This includes setting goals and breaking them into smaller steps.

4. Action: Based on the formulated plan, the AI performs multi-step tasks, interacts with external systems, and dynamically changes the plan to fit a changing environment.

5. Reflection: After taking the planned or altered actions, the AI learns the results from received feedback and perceives changes in its environment. It evaluates the effectiveness and success rate of its course of actions, and uses the output to adjust its next cycle of: perceive, reason, plan, act, and reflect. This is what allows the Agent to adapt and improve over time.

The words "AI agent" and "Agentic AI" are used most of the time interchangeably, but the former generally is more specific to the AI model, while the latter implies the system that the AI agent is operating within.

[2] The Probabilistic Nature of Current AI Models

Probabilism means the absence of certainty, or the presence of randomness. In the context of technology, it would mean that a certain function might give a different output when given the same input. The opposite of this concept is determinism, the same output for the same input every time, the output is determined by the input.

Contemporary AI models use the concept of probabilism to take the large amount of data that they have been given and test, match, and generate new content and actions from this data. It means that every time an LLM or AI agent is given the same input or prompt, it is likely to produce a different output or Response.

Internally, an AI model would give different probabilities to different possibilities based on a large number of parameters and the algorithms integrated within. This allows the AI to predict what is most likely correct according to the real-world data that is often incomplete, unclear, or noisy, allowing it to make better decisions, predict outcomes, and solve problems. Another key important factor would be "model shift," the change that the model goes through from continuous learning, which would change the outputs and responses of that model.

[3] Guardrails and Their Application on AI

Guardrails have become a fundamental concept in the field of AI. A guardrail is a control mechanism used to restrict the freedom of the AI model to ensure it is working safely, responsibly, and within defined boundaries. It does so by enforcing policies, technical controls, and monitoring mechanisms on simple AIs, LLMs, or AI agents. These guardrails can be split in many ways and many types to accommodate and safeguard the expanding functions of AI. Four types of guardrails can exist across every layer of AI use, including:

Data guardrails: Cleanses datasets from sensitive information and validates training data, aiming to reduce bias and enforce data privacy rules. This ensures that models are trustworthy and ethical.

Model guardrails: These handle metrics such as latency, toxicity, accuracy, and robustness that are used to measure real-world performance, fine-tune, and optimize the model's behaviours.

Application guardrails: There are also application-specific guardrails for apps that integrate an AI model in their functions, such as a chatbot. They use Application Programming Interfaces (APIs) to enforce policies, block harmful or AI-generated content, validate sensitive data, or restrict how AI tools work within a specific context.

Infrastructure guardrails: This type of guardrail functions similarly to the application ones but on the scale of systems, cloud, and the network layer. The organization applies security practices such as access controls, encryption, and Logging. Infrastructure guardrails ensure the protection of the environment within which the AI works.

Guardrails can also be taxonomized by their placement, be it internal or external to the AI model. Guardrails are also designed to protect from a wide and growing variety of cybersecurity attacks, and a few cybersecurity frameworks have already aggregated and

[4, 5] triaged common attacks on LLMs and AI .

[6] Governance and Security

Governance, security, and compliance are often intersecting fields that impose strict rules and policies on different systems and industries. These rules are strict and clear, and they

require the system on which it is based to be auditable with clear accountability and decision making, but since the nature of modern AI systems relies so much on probabilistic reasoning and behaviour, it contradicts the transparent and explicit requirements that governance and regulations need to function.

From a security point of view, these AI models introduce new risks by their unusual nature of operations, and reintroduce older ones by increasing or refreshing the surface of attack for systems employing AI help. The weakest link in cybersecurity is often said to be the human, but with the introduction of AI, we get a new link that not only mimics human intellect but also its weaknesses. Traditional systems relied on strict and deterministic rule sets or polices, describing who can do what, but with how "smart" an AI can be and with how many permissions it can be given, its randomness and unpredictability can make it the weakest link in the chain of security.

The Gap Between AI Agents and Policy

The gap between the interleaving of these systems forms mainly from the probabilism and dynamism of AI models. Regulatory frameworks and governance bodies need clear accountability, consistent traceability, convenient auditability, and reproducible decisions, which fit a traditional deterministic enforcement workflow, but contradict the nature of AI models, creating a gap between AI and policy enforcement.

Existing controls or guardrail mainly work by altering the behaviour of AI models indirectly and lack the ability to be explicit and match the dynamism of these AI models, as the goal of security should be to minimize risks and threats while keeping friction to a minimum, and a lot of frameworks and laws promise not to stifle the freedom of AI model, but a clear and transparent implementation that satisfies all of the criteria is still lacking the current landscape of AI guardrails.

1.1.2 Synopsis

This documentation presents a novel guardrail architecture that uses the general-purpose

[7] decision-making engine Open Policy Agent (OPA) . OPA is generally used in Development Operations (DevOps) for applying policy over the deployment of infrastructure, CI/CD pipelines, and the cloud. Its developers describe it as “an open source, general-purpose policy engine that decouples policy decision-making from policy

[7] enforcement” . In this Project, it plays a critical role as the heart or middle layer of the

guardrail's architecture that specializes in governing the operations of an AI agent and its working environment.

The proposed design and implementation focus on core security principles such as Zero- Trust, by separating each of the main functions--detection, decision-making, and enforcement-- to a separate layer decoupled from the rest; Human-In-The-loop (HITL), by explicitly requesting the supervision of a human in certain critical cases; and Role- Based Access Control (RBAC), by applying context- and session-aware decision-making.

It has also consulted globally recognized standards, regulations, and security frameworks

[8][9][10] such as ISO/IEC 42001 , EU AI Act , OWASP Top 10 LLM , and MITRE ATLAS

[11] in its design and implementation to inspire many of the features and requirements of the architecture, a few examples: previously mentioned security principles, Logging, artifact generation, probabilistic-to-deterministic translation, and policy lifecycle, which

[7] made the OPA engine and Rego, declarative Policy-as-Code (PaC) language , the natural choice that can feasibly support the framework of this policy-driven guardrail.

1.1.3 Motivation

The main drive behind this Project came from our observation of common emerging attacks targeting the newly adopted AI helpers in the cybersecurity world, some of them describing how companies can be hacked by only using their AI agents. Another big motivator is curiosity about the newly created field of securing AI that seems ripe with opportunities for innovation and new discoveries. Besides that, we aim to ease the burden of implementing an AI based database helper for companies for all sorts of roles, including database admin, HR analysts, and employees inside the company. Lastly, our desire to contribute to the cybersecurity field, especially the open-sourced part of it, is to provide an open-source community-scalable solution to address the current gap in AI governance.

1.2 Problem Statement

A few critical problems related to database management, query engineering, and table or database architecture often muddy the user experience between the database system and all sorts of roles that need to use it. AI agents, with its actionable capabilities that interact with real systems, can help all of these roles achieve better efficiency and accuracy than traditional methods of memorizing query syntax and long equations or statistic principles.

On the other hand, emerging risks involving AI are growing in frequency and impact synchronously with the increased integration and reliance on agentic AI systems in operational and critical workflows for databases, particularly those involving security, governance, and accountability, which are struggling to put effective controls and constraints on AI agents working within these larger systems. This section will present an overview of the problem as a whole and its surrounding context.

1.2.1 Problem Description

The current literature and updated industry practices acknowledge the growing risks introduced by agentic AI systems, and these include a wide range of standards crossing security, operational management, governance, law, accountability, etc. The current literature is also discussing a wide array of mitigation mechanisms, including model alignment, prompt engineering, behavioural guardrails, and effect monitoring. All these approaches have been proven to improve the state of Agentic security and compliance, but they largely operate on the same layer as the AI agent rather than forming an independent system to detect, decide, and enforce explicitly and obviously implemented controls or polices.

Current frameworks are by nature deterministic and aim to be repeatable, objective, and transparent in their functions, requirements that are difficult for autonomous AI agents running with LLM to satisfy, considering the dynamic and adaptive nature of their actions. The absence of a standardised and system-wide control mechanism is resulting in a high- risk deployment in current organizations that want the proven productivity boost that comes with utilising autonomous workflows.

Thus, there appears to be a gap between the deterministic frameworks and probabilistic workflows that needs to be bridged with minimal friction and maximum effectiveness. As in, the control would need to correctly implement its function, while leaving the underlying Agentic AI system unmodified.

1.2.2 Desired Outcome

The outcome that this Project aims to achieve is to design a policy-centric control mechanisms architecture for agentic AI systems on databases that can be extended, reused, made compatible with existing models, and even future ones by security engineers. This control mechanism is in the shape of a deterministic and explicit guardrail that is made of a security architecture that logically separates the functions of detection,

decision-making, and enforcement, enabling maximum flexibility and extendibility of the system.

This work is not a user-facing system; it is a back-end security control that would be employed inside an environment running AI agents. It would work in tandem with other such security controls, such as network monitoring tools, firewalls, and endpoint/browser detection and Response.

1.2.3 Target Audience

The implementing audience of these security controls is system architects and DB admins, BI analysts, HR professional, security engineers, and governance teams working to secure the active deployment of an Agentic AI system. These stakeholders are responsible for planning, tweaking, and applying the proposed guardrail architecture on the deployed AI systems to secure them or to follow legal or industrial compliance.

The contributing audience is the stakeholders interested in adopting the proposed architecture to apply a practical, feasible, and enforceable approach to effective governance over AI using Databases. These stakeholders can be policymakers, auditors, researchers, open-source contributors, and standard bodies that care for reducing risks, visibility, and gaining control of agentic AI behaviour in a structured, objective, and systematic way.

1.3 Significance of the Project

The significance of this proposed work lies in its purpose of accommodating the continuous trends in the technological landscape when it comes to the additions of technologies for legacy or old-world systems specifically database, a trait that cybersecurity as a field follows with its generally proactive nature. The idea of this project came as a reaction to the current landscape to reflect the need for security and trust in the field of AI as a whole, which has proved its worthiness when it comes to increasing productivity, but it has also shown how this newly introduced Risk impacts an organization's unprepared security posture.

Currently, one of the main challenges is minimizing the attack surface that the implementation of an agentic AI introduces into a database system. An AI agent that has extensive and sprawling access permissions and varied tool usage can be externally facing, whether that happens intentionally or not; it makes for a crippling risk for a security posture.

A recent real-life example of the dangers would be an incident reported by Anthropic. The AI American-based company has reposted that their AI agent "Claude" was used by a Chinese cyber espionage campaign that targeted American companies by using "vibe- hacking," which is a way that cybercriminals weaponize AI models to perform the cyber- attack chain lifecycle, even if the user has no technical knowledge on the subject of

[12] hacking . His campaign used an integrated AI agent that companies employed without side-facing interfaces to conduct all stages of their attacks after the campaign initialization, including reconnaissance, vulnerability discovery, lateral movement, and

[12] finally documentation and handoff .

These incidents encapsulate the current state of AI security and the scale of havoc that an unsecured or unmanaged AI agent can wreak on an organization's security, be it by being abused by a malicious actor or by hallucinating a deletion command for the entire

[13] database. Those are the types of incidents that this work aims to address and mitigate, contributing to the current field of cybersecurity and AI governance, and demonstrating practical, real-life applications of the proposed guardrail.

1.4 Project Objectives

The objectives of this work are as follows:

1. To assess and analyse the current limitations of existing guardrail solutions that are being applied to agentic AI systems, preferably over databases.

2. To design a novel policy-driven architecture that is deterministic in its workings and controls.

3. To implement a guardrail that satisfies core security principles such as Zero- Trust, HITL, and RBAC.

4. To demonstrate how probabilistic actions can be controlled and translated to deterministic enforcement

5. To align the guardrail with current industry frameworks and global standards for cybersecurity and AI governance.

6. To propose a database specific solution that improves auditability, accountability, and trust in a system that uses autonomous AI when it comes to databases.

1.5 Project Contribution

The proposed architecture aims to provide a useful and novel way of securing AI and governing it.

1. Novelty in the idea

The primary novelty of the proposed perspective lies mainly in treating the problem of agentic AI governance as an issue of determinism that contradicts probabilism rather than an issue of the model itself or its alignment. By framing the control of AI systems as an explicit first-class process, rather than an afterthought, the Project introduces a new way of approaching AI security that aligns with established cybersecurity principles.

2. The audience that it serves and how

As mentioned above, the main target of this Project is our implementing audience and our contributing audience. Also, it will serve any high-risk or critical organization that has strict and rigid regulatory requirements, such as financial institutions, hospitals, and private companies, looking to enhance their workflows by implementing automation mechanisms and AI systems while also applying RBAC and AuthN. It provides them with a practical and extendable blueprint that they can shape for their needs, systems, and security requirements.

3. Novelty in the choice of the model

The use of OPA and Python as the middle layer and deterministic decision point of our architecture fit naturally with the existing properties of the general-purpose policy engine, and it represents an accurate but novel choice of an already mature open-source project with wide support and general or transferable skills, as DevOps engineers, the main users of OPA, can contribute greatly to the implementation of the guardrail with their already earned skills and repurposed experience.

4. Novelty in the structure of the pipeline

Finally, the proposed security architecture or pipeline that logically separates detection, decision-making, and enforcement offers clear and transparent structural separation of functions, concerns, inputs, and outputs that is commonly missing when it comes to existing guardrail solutions. It also supports the modularity and extensibility of the content

of each layer. All of these traits ensure the upholding of the core concepts of this Project: determinism, consistency, trust, and Transparency.

1.6 Outline of the report

This document has four total chapters past the cover and abstract, each one discussing a specific topic, including concepts, research, planning, and design of this Project:

Chapter 1:

This first chapter provides a high-level overview of the Project, its nature and required knowledge background, objectives that this Project aims to achieve, and what problems it is aiming to solve, and how that contributes to the field of cybersecurity as a whole.

Chapter 2:

The second chapter demonstrates the project planning structure including the final project deliverables, the tasks that need to be completed and their timeline, graphs and tables to visualize the timeline and dependencies, roles of each team member, task associated risks and their remediations, the required and optional costs incurred by the implementation of this Project, and any professional or technical tools used in the designing and management.

Chapter 3:

The third chapter discusses in detail ten different implementations and paradigms related to the main subjects of this documentation, forming a wide and varied literature analysis and review. Following that, it discusses the shortcomings and knowledge gaps of those works fairly and honestly, then it defines the criteria used to compare all of those works, and finally, it demonstrates how this Project can theoretically achieve all of those criteria.

Chapter 4:

The fourth chapter handles the subject of requirement specifications, which includes identifying stakeholders and their importance, software and hardware platform requirements that are needed or recommended to run the designed system, requirements related to the functions of the system, requirements related to the environment of the system, and any other requirements that do not fall into those sections.

Chapter 5:

The fifth chapter holds a very significant part of this document as it included a verity of illustrative diagrams, some abstract, others detailed and physical. It aims to provide a full view of this project, running from an overview of its main functions, use-cases, dataflow, and how the project will be implemented in a real production system.

Chapter 6:

The sixth chapter handles talking about the implementation details, it mentions the general specifications like the programming languages, libraries, APIs, and any other technologies that were used in the development and implementation of this project to reach a functional fully realized state that can be tested and measured for the next chapter,

Chapter 7:

The seventh chapter plays directly off the back of the previous chapter as it lays the ground of a measurable and quantifiably testing method that was used to figure out the effectiveness of the design and implementation of the project. This serves the purpose of checking how much of the original objectives were reached, and how does the project compare to other similar projects that were compared in the third chapter of this documentation.

Chapter 8:

The final and eighth chapter begins by giving a final condensed summery of the whole of the documentation focusing on the final results and any additional opinions of the writers. Then, it finishes with a bunch of recommended direction for progress or development of this project. Some of these directions were un-realized feature, or new features that were out of the scope of this project from the start.

## Chapter 2 Project Plan

2.1 Project Deliverables

The following is a list of deliverables of our guardrail implementation project:

The policy as code rule-set:

This rule-set is the heart of our Project. It will be written in Rego, a language specifically designed for the OPA engine. We aimed and created a comprehensive set of RBAC rules inspired by the OWASP LLM Top 10 List to fill its content gaps. We made them tailored to our database AI application.

The decision point:

The OPA engine itself is running on our demonstration hardware without any modifications to its internal functions.

The enforcement point:

[7] The OPA is a decision-making engine; it does not enforce the policies itself . It is part of a larger system, and another part of that system is the enforcement point that will carry out any actions required after the decision-making process. This part is entirely composed of a python server.

The system’s architecture:

This describes the logistics and technical implementation behind how this system will connect, and where each part will be in relation to the other parts and endpoints, like how the user's prompts will pass through the engine, how the AI agent will be directed to send its Response back for analysis, and how the output of the Response or action will be displayed.

Logging and Auditing architecture:

An important part of our Project is producing auditable logs, records, and artifacts that we can reference for telemetry, forensics, and system debugging. This also goes along with

[8] the ISO/IEC 42001 standard . These logs are sent to the ELK stack to be normalized, indexed, and displayed.

AI agent:

Nanobot AI agent with Gemini-3.1 as its brain was chosen to play the part for demonstrating the capabilities and effectiveness of the policy guardrail. It would need to have basic agentic capabilities, such as being able to do the following: receive text prompts from the user, work autonomously based on assigned duties, perform required actions, interact with the database server, and receive feedback to adjust actions.

User interaction point:

The interface, in this case Telegram, that the user will use to send prompts to the AI agent, receive outcomes or feedback from actions, edit and debug PaC files using and IDE, and view logs and triggered rules using an ELK based dashboard. These interfaces ensure a strict security and authentication mechanisms are implemented with RBAC to protect the system's sensitive functionality.

The project documentation:

The document that is being read now, along with any required appendices, will supplement the information here. The aim is to create comprehensive, relevant documentation for our Project, to serve as a reference point for others and for us.

Containerized Environment & Source Code:

The containerized deployment with all containers that is made of a docker compose and build file along with the main source code for the project’s middle connection layer that routes traffic across the docker container network.

2.2 Project Tasks

We have set a flexible, planned strategy suitable for a small team working closely together. We aim for an agile, recursive methodology to guide our strategies, implementations, and decision-making. The table below demonstrates the different stages and substages that the Project will go through, along with the required time and stage dependencies:

Table 2-1: A table describing required tasks

TaskTask Name Time Dependencies ID Analysis

A1 Topic Research, Feasibility & Initial Literature Review 3 Weeks None

A2 Regulatory & Law Analysis (EU AI Act, ISO/IEC 42001) 2 Weeks A1

A3 Extended Literature Review & Resource Collection 4 Weeks A1

A4 Threat Modelling (OWASP Top 10 for LLMs 2025) 2 Weeks A3

Design

D1 Guardrail Policy & System Architecture Design 3 Weeks A3

D2 Decision Logging & Auditability Design 2 Weeks D1

D3 High-Level Enforcement & Control Flow Design 2 Weeks D2

Learning & Foundations

L1 Policy-as-Code, Rego & OPA Fundamentals 4 Weeks D3

L2 AI Models, Agents & Tooling Fundamentals 4 Weeks D3

Prototyping

P1 Initial Guardrail & Policy Prototypes 4 Weeks L1

P2 Agent–Guardrail Integration & Middleware 4 Weeks P1, L2

P3 Enforcement Points & Decision Logging 4 Weeks P2

Refinement & Optimization

R1 Policy Refactoring & Deterministic Enforcement Validation 4 Weeks P3

R2 Testing, Edge Cases & OPA Optimization 4 Weeks R1

Finalisation

F1 System Evaluation & Experiments 2 Weeks R2

F2 Documentation, Figures & Final Write-up 3 Weeks F1

The Gantt chart below represents the timeline for the analysis, design, and creation of our Project, the policy-driven guardrail:

Figure 2-1: A Gantt chart visualizing the project timeline in weeks

2.3 Roles and Responsibilities

To finish our Project promptly and produce our best possible result, we split the work among the three of us in the following manner:

Table 2-2: A table showing each team member and their roles

Team Member Roles and Responsibilities

Project Management Communication Management Project Deliverables Osama AhmadSystem Design Methodology Regulatory Standards Research Charts and Graphic Design

Gathering of Resources Cost Estimation Proof Reading Ahmad Al-Surakhy Project Management Tools Meeting Management Tool’s Feasibility Research

Risk Assessment Compliance Assurance Ethical-Standards Auditor Omar Al-Jaafreh Legal-Standards Auditor References Management Knowledge Gap Assessment

Report Writing Report Design Presentation Design SharedSystem Architecture ResponsibilitiesSystem Requirements Feasibility Analysis Practical Implementation Testing/Debugging

2.4 Risk Assessment

To manage and demonstrate our commitment to the functional, ethical, and legal sides of our Project, and our care for the Project's stakeholders, we made this table that aims to define and assess any risk that might threaten the Project's operations, with minuscule risks having already been omitted:

Table 2-3: A table assessing risks for each of the operation stages

TaskRisk Description RiskImpact Likelihood IDID

Analysis

Scope Creep: Failing to define the scope of the Project might leadAlmost A1 R01 Major to the slow creep of its scope until it becomes unmanageable. Certain

Lack of Stakeholder Involvement: A lack of targeted stakeholder R02 Major Possible involvement may lead to misalignment with project goals.

Regulatory Skill Gap: The project team might lack the necessary expertise to understand and implement standards such as theR03 Major Likely ISO/IEC 42001 A2 Dynamic Standards: International standards of technology often Almost accommodate the fast-shifting industry, making them very dynamicR04 Moderate Certain and ever-changing.

Information Overload: Spending too much of the team's time gathering resources can lead to wasted time or simply getting lost inR05 Minor Likely A3the information. Access Limitation: Some valuable resources might be locked R06 Minor Possible behind paywalls or proprietary licenses.

Inaccuracy of Reference: The OWASP Top 10 Lists often focus A4on theoretical attacks and may be influenced by the writers'R07 Moderate Possible

[10] subjectivity .

Design

Over-Engineering: Creating a design that is too complex will hinder implementation and make the system harder to maintain andR08 Moderate Likely scale. D1 Traffic Redirection Difficulty: A major part of the design is how the different subsystems will interact through the central point (TheR09 Major Possible Guardrail).

Data Analysis Privacy: Deciding how much data to analyse R10 Severe Unlikely according to the laws of legality and ethics

Data Log Privacy: Deciding how much data to log according to the D2 R11 Severe Likely laws of legality and ethics

Fail Unsafe: The system might let all traffic pass and go unchecked R12 Severe Possible if it fails. D3Latency and Friction: The system will increase the number of Almost hops that the traffic will take, which will increase the amount ofR13 Major Certain latency and user friction.

Implementation

Learning Curve: Learning a new language introduces many Almost I1challenges, especially since this one is a declarative language ratherR14 Moderate Certain than an imperative one.

Integration Friction: New and unaccounted difficulty might appear while implementing the guardrail and connecting it to theR15 Moderate Likely other subsystems. I2 Standardization Issues: Issues regarding the type of traffic that is sent, what format it will be in, what protocol will be used, and howR16 Moderate Possible

much of it will be sent. Model Drift: The change of the AI model over time as it is being continuously trained during all the different phases, makingR17 Minor Likely benchmarking difficult.

Creative Nature: AI models, by their nature, aim to generate I3Almost content in different formats, which requires an element ofR18 Moderate Certain randomness and "creativity", making benchmarking difficult.

Implementation Difficulty: A mix of a lack of expertise, the R19 Major Likely overwhelming choice selection, and the time crunch.

Software Vulnerabilities: The point of enforcement might be

bypassed and enumerated, as the AI agent might be manipulated to R20 Severe Likely craft special prompts to bypass, recon, or even perform Remote Code Execution I4 False Trigger: The possibility of False Positive or False NegativeAlmost R21 Moderate results. Certain

Bottleneck Formation: The enforcement point becomes a R22 Major Possible bottleneck for the traffic.

Time Crunch: The amount of limited time, cutting the testingAlmost I5 R23 Major phase short, which has the potential of missing edge cases. Certain

Trade-Off paralysis: Choosing between more complex rules and a R24 Minor Likely reduction in latency. I6 Bug Introduction: Changing the configuration this late might R25 Moderate Possible introduce new bugs.

The following table is a continuation of the previous one that records possible mitigation strategies we are willing to implement to solve or reduce the risks that our work is exposed to in any of the three stages:

Table 2-4: A table describing mitigation strategies for discovered risks

Risk ID Risk Name Mitigation Strategy

Analysis

Establish a strict timetable and project documentation while utilizing the "Do R01 Scope Creep I really need this?" mentality. Lack of StakeholderRead up on any news articles concerning past incidents related to AI agents, R02 Involvementask university instructors for advice, and read about social media cases.

R03 Regulatory Skill Gap Utilize open sources on the web, and ask university instructors for advice.

Write policies that outline general principles and leave room for flexibility R04 Dynamic Standards and refactoring.

Force a time frame for information research by upholding a "Pencils Down" R05 Information Overload approach. Allocate a backup budget for accessing proprietary solutions, while R06 Access Limitation considering open-source alternatives.

Cross-reference the OWASP Top 10 lists with real-world incident databases, R07 Inaccuracy of Referencesuch as the MITRE ATLAS, to ensure the observed attacks reflect real-world

[4, 5]. cases, not just theoretical ones

Design

R08 Over-Engineering Start with the bare minimum architecture and add to it in a modular way.

Traffic RedirectionUse a Sidecar architecture or API Gateways to intercept traffic, decoupling R09 Difficultythe guardrail logic from the main application code.

Practice Data Minimization: only collect the data you need when you need it. R10 Data Analysis Privacy Along with Transparency, to ensure ethical and legal validity. Implement Access Control and Log Hygiene, automatically hash or mask R11 Data Log Privacy patterns resembling PII before writing to log storage.

Implement a "Fail-Safe" Default to prevent traffic from passing through if R12 Fail Unsafe the guardrail goes down. Enforce the Latency-Target to ensure latency remains within acceptable R13 Latency and Friction parameters.

Implementation

Use the OPA Playground for rapid learning and testing, while leveraging R14 Learning Curve (Rego) pre-made libraries to skip boilerplate code.

R15 Integration Friction Define the required specifications for all subsystems before starting coding.

Ensure the matching of the JSON format between the guardrail and the Agent. R16 Standardization IssuesEnforce output parsers on the Agent to ensure it always returns a JSON format. Use

[14] OpenAPI/Swagger .

Use specific model snapshots rather than the latest version to ensure R17 Model Drift consistent behaviour during development.

Set Randomness/Temperature to 0 for the duration of the development and testing. R18 Creative NatureCreate a dataset of expected prompts and responses to benchmark the guardrail

[15] against. Use Pydantic .

[16] ImplementationUtilize existing open-source guardrail architecture (e.g., NVIDIA Nemo , R19 [17] DifficultyGuardrail AI ) instead of building things from scratch.

Conduct penetration testing to ensure the system is protected against known R20 Software Vulnerabilities [18] vulnerabilities and blind spots. Use Garak . Control the scope of the Policy file, and ensure relevant telemetry gets R21 False Trigger collected for continuous optimization.

Ensure a possible addition of a load balancer and horizontal scaling for the R22 Bottleneck Formation enforcement point. Distribute the work evenly among team members. Consider shifting it left a R23 Time Crunch bit to gain more time.

[19] Utilize the Risk Matrix and the stakeholder analysis to set SMART goals R24 Trade-Off Paralysis and make relevant decisions. Use "Shadow Mode" Deployments and Version Control to test and maintain R25 Bug Introduction the ability to roll back.

The risk matrix is an auditing tool designed to help visualise the severity and likelihood of various risks at a glance. Using this Matrix, we can prioritise these colour-coded risks, leading to efficient mitigation and treatment:

Table 2-5: A matrix visualizing the severity and priority of each Risk

Likelihood Almost Likely Possible Unlikely Rare Certain

Negligible

R05, R17 Minor R06 R24 R04, R14R07, R16 Moderate R08, R15 R18, R21 R25 Impact R01, R13R02, R09 Major R03, R19 R23 R22

Severe R11, R20 R12 R10

2.5 Cost Estimation

The table below shows the two valid financial paths we can take for our Project:

The first is dependent on a proprietary AI Interface and cloud hosting. This would allow us to gain access to an AI agent for a limited number of queries and a cloud

infrastructure to demonstrate a comprehensive enterprise guardrail solution.

While the other option depends entirely on hosting the AI agent locally and using local hardware, which would allow us total freedom at zero cost, it places the entire infrastructure overhead on our team, and the AI agent might be too weak to fully test our system. We can still use the first option as a backup.

Table 2-6: A table comparing the prices of the two extremes Category High-End Estimate Low-End Estimate

[20, 21] [22] AI Brain $50.00 (GPT-4o/Claude 3.5) $0.00 (Ollama - Llama 3)

[23] [24] Hosting $20.00 (AWS EC2) $0.00 (Docker)

[25] Computing $10.00 (Google Colab) $0.00 (Local Hardware)

[26] Proofreading $30.00 (Grammarly) $0.00 (Manual Proofreading)

Total $110.00/month $0.00/month

2.6 Project Management Tools

1. Time tracking and project management

a. Google Calendar: Used for scheduling regular team meetings, tracking milestones, and working around busy periods of fellow team members.

b. GitHub: Useful for managing the projects code files, and to find resources.

2. Collaboration and documentation

a. Microsoft Word: The main document creator and editor used.

b. Microsoft Excel: The main table creator and editor for our Project.

c. Microsoft PowerPoint: Used for creating the presentation files.

d. PDF Reader: Essential for reviewing academic papers and such.

3. Applications for Meeting

a. Discord: Used as the primary platform for daily internal communication, enabling the fast exchange of messages by text, audio, or call.

b. Zoom: The backup meeting software. It is worse than Discord in every way.

4. Diagram and Graphic Tools

a. Lucid Charts: The main graph and diagram maker. It is a web-based chart editor.

b. Microsoft Visio: The backup diagram and graph maker.

5. Implementation Tools

a. OPA Sandbox: Provides an isolated, web-based development environment for rapid prototyping and Rego policy code creation before being deployed to the local

[27] environment .

b. Visual Studio Code: Used as the main Dev Environment. It will be used with to write, debug, and implement the source code for the PaC and the project.

c. Docker: User for containerized application deployment

d. ELK Stack: A forensic engine used for centralized logging and visualisation.

e. Redis: A fast in-memory database used for session context, and users’ profiles.

f. Nanobot: A minimalist open-source Ai agent framework.

g. Telegram: A chat app. User as the ID provider and the main user chat UI.

## Chapter 3

## Literature Review and Related Work

3.1 Related Work

In this chapter, a literature review is presented on a number of related works. This review will present an overview of previously published works on different ways to guard AI models. It will summarize the work and identify the limitations and shortcomings, which will be used in the following chapter to form a knowledge gap.

1 ReAct: Synergizing Reasoning and Acting in LMs (Yao et al., 2022)

ReAct (Reason + Act) is a paradigm that was introduced in 2022 by a group of Google researchers. It represents a thinking approach used by Artificial Intelligence that can allow it to generate reasoning traces and task-specific actions in an interleaved way. So, instead of simply, randomly, or creatively generating text in one go, an LLM utilizing the ReAct paradigm would be able to "think" about the problem, execute an external tool at its own

[28] discretion, evaluate the output, and then refine it .

It aims to mimic the human relation between putting thoughts into words (verbal reasoning) and their connection to related task-oriented actions. An example of this would be a chef cooking up a dish. Between any two distinct actions, the chef can verbally reason to track his progress ("I finished cutting the vegetables, now I should boil the water."), to handle changes and exceptions ("I don't have salt, so let's use soy sauce instead."), and to realize any limitations or needs of external information ("I need to open the cookbook to check the recipe."), and then put that reasoning to use to carry out reasoning-supported

[28] actions ("What dish can I make right now with what's available?") .

2 NeMo Guardrail (NVIDIA, 2023)

NVIDIA NeMo Guardrails are a part of a larger open-source toolkit for developing entire LLM-based systems. The guardrails tool, part of the toolkit, provides the ability to add programmable guardrails using a custom language called "Colang" to define conversational flows and enforce policies internally. It focuses on monitoring the input and output to alter the flow of the conversation to ensure that the conversation stays within the allowed context and safety borders (e.g., preventing a Customer Support chatbot from

[29] discussing political conversations) .

3 Purple Llama (Meta, 2023)

The Purple Llama is Meta's umbrella project that includes a multitude of security and safety tools for the initiative of protecting and securing open generative AI models. Its goal is to provide developers with open-source tools, safety models, and security frameworks that help developers build and initialize safer LLM systems, with more future tools planned. The purple in the name refers to the fact that it mixes both red and blue cybersecurity concepts to provide both attack and defensive postures. In the next paragraphs, we will talk about a couple of the relevant defensive (blue) tools, along with

[30] the framework to bring them together .

Llama Guard, and its many versions, is a safeguard in the Llama ecosystem, and it is one of the core safety models that Purple Llama provides. It focuses on classifying input/output for Human-AI Conversations, and it does so by utilizing LLM and its default but flexible taxonomies (e.g., Violence & Hate, Sexual Content, etc) that get applied to prompts and responses separately, which is not always consistently addressed by

[31] commercial moderation tools (e.g., Azure Content Safety) .

Prompt Shield, or Prompt Guard, is another safeguard in this ecosystem. It specializes in defending against prompt-based attacks, such as prompt injection and jailbreaking, rather than moderating and categorizing input/output like Azure Content Safety and Llama Guard. Prompt Shield also uses an LLM that does not rely on fixed signatures or deterministic rules; instead, it estimates the probability of a malicious prompt that aims to trick agents into exfiltrating data or performing unauthorized actions outside the model's intended behaviour. It has a very narrow focus on malicious inputs, rather than

[30] broader harmful categories .

Llama Firewall is not a single safeguard, model, or tool, but it is a safety and governance layer for the entire system that acts as an orchestration and enforcement point around LLMs, particularly those with agentic capabilities. Rather than acting as a single guard point, the firewall aggregates signals from the previous probabilistic safety guards (Llama Guard, Prompt Shield) and applies deterministic policy-driven controls to requests. By sitting between user input, AI model interface, and downstream actions, Llama Firewall makes policy-driven decisions such as blocking, routing, sanitization, or restricting based on assessed Risk. This hybrid mix allows for flexibility and growth from the probabilistic aspects, and allows for predictability and auditability that come from the deterministic

[32] aspect introduced by this Firewall .

4 GuardAgent (Xiang et al., 2024)

GuardAgent is an LLM agent designed to act as a guardrail for other LLM agents. It governs the target agent by analysing its inputs/outputs to check whether they satisfy a set of user-given safety requests called "guard requests" (e.g., safety rules or privacy policies). These requests are defined by the user in Python and are executed with an API call for the guard LLM. It works by dynamically monitoring and enforcing safety requirements on their actions and outputs. It uses the user-defined guard requests to create an action plan, and then generates the executable guardrail code based on the user's request and given context to enforce compliance in real-time using that specific context

[33] .

GuardAgent also leverages a memory module to improve understanding of diverse user requests over a period of time. It also supports a set of extendable tools and functions and an API that allow it to adapt to new domains and requirements without retraining the underlying model. So, the main function of this LLM is to create guardrail code based on given natural language requests and agent context; Rather than use the LLM to directly

[33] enforce the rule set .

[34] 5 Traditional Database Security and Access Control

Before AI with tool calling and third-party system integration was a thing, databases relied solely on mature, hard, and deterministic access control frame works, most commonly Role-Based Access Control (RBAC), and Row-Level Security (RLS). Database systems like PostgreSQL or MySQL security gets reenforced through rigid, and very static permissions that aim to define permission scope through specific verbs such as Select, delete, etc. These verbs are getting applied to objects usually tables. As explained many times in this document, a rigid system such as this will introduce a lot of friction when introducing an inherently dynamic system such as AI systems. The database is part of a bigger environment. It does not have visibility or knowledge to the rest of the

[34] system. So, it can only apply its control over itself .

[35] 6 Agentic Data Interfaces and Text-to-SQL Implementations

Continuing on with the time-line here, when AI did become a thing, specifically when agentic interfaces that can connect AI brains with external tools, a shift toward automations and ease of use happened, allowing non-technical users to query complex databases using natural language without a hint of extra mental usage. However, these

implementations introduce common issues despite the obvious benefits of automations and ease of use. These issues include: granting the AI broad and high-level privileges so it can serve all users. This creates an issue where the AI system is not operating with in basic security fundamentals such as least privilege as there. These issues expose the

[35] system to large scale prompt injection, and destructive hallucinations .

3.2 Knowledge Gap

3.2.1 Critical Analysis

The literature reviewed in the previous section demonstrates significant progress over the last few years in the development of guardrails for large language models and agentic AI systems. At first, researches tackled the challenge of creating a reasoning paradigm that can allow these models to “think” and “act” based on their training and environmental feedback among other things, but a need for extra layers of defence, detached from the reasoning trace of the target model appeared, to ensure robustness, truthfulness, and safety

[28] of the model’s actions and interactions .

Early approaches to implementing a security parameter or a guardrail focused mainly on input/output filtration or moderation, as seen in systems such as NeMo Guardrails. which all aim to prevent harmful or policy-violating content through classification, validation, or conversational flow control. While effective at constraining textual interactions, these approaches operate largely at the surface level of LLM inputs and outputs, providing a rigid and limited control over the internal decision-making processes and actions of

[29, 30] autonomous agents, partially caused by their chosen scope and deterministic nature .

More recent approaches have extended these guardrails to include agentic AI systems, and they did so by monitoring actions, tool usage, and execution traces. These works include frameworks such as Llama Firewall, and GuardAgent which introduce runtime enforcement mechanisms that govern agent model behaviours beyond content filtering, into contextual and role-based authorization. However, these systems and frameworks predominantly rely on probabilistic models, adaptive learning, or LLM-generated enforcement logic. As a result, their behaviour is inherently uncertain and is difficult to predict, reproduce, audit, and accurately benchmark, especially in a safety-critical or regulated environment where deterministic guarantees and transparent decision making

[31] are required .

3.2.2 Shared Gaps

Across the surveyed solutions, a recurring limitation starts to emerge in how probabilistic risk assessment and deterministic policy enforcement are structured and governed. While several systems, such as GuardAgent, and Llama Firewall, do include some type of deterministic enforcement mechanisms, they are typically tightly tied to a probabilistic backbone made of detection/categorization models, LLM-generated logic, and application-specific control flows. As a result of that, policies are not treated as discrete, explicit, and authoritative functions, but rather as implicit behaviours attached to these models and their generated outputs. This coupling may increase adaptability and functionality, but it limits explainability, reproducibility, version tracking, and systematic governance.

From another angle, connecting an autonomous agent with a deterministic and rigid system such as a database introduces what is known as the “determinism gap,” where one system requires absolute certainty and formal proof for authorization for every action to ensure integrity and non-repudiation, while the AI operates in a probabilistic plain of reasoning that can hallucinate an authorized user’s actions. Thus, introducing risks and justifying the need for a formal external policy-guardrail that deconstructs the agents’ actions and turns them into signals that can be judged.

These gaps highlight the need for a policy-driven guardrail architecture that enables deterministic, auditable, and context-aware governance of agentic AI systems. Such an approach should decouple probabilistic safety signals from enforcement logic and decisions, providing a general multipurpose declarative mechanism for expressing and enforcing traceable user-defined policies across agents' actions, tool usage, and multi-step workflows. Addressing this gap forms the motivation for the proposed Project in this documentation.

3.2.3 Comparative Analysis

Table 3-1: Legend for the following gap matrix showing chosen criteria and their meanings

Symbol Definition Type ✓ O ✗

Does it Separate detection| decidingAppliesPartialNo architect Sep Architectural |enforcement? Zero-Trustseparationseparation

ExplicitlyImplicitly Vague or Policy Does it have explicit Policy representation Architecturaldefined asdefined or embedded artifactslearned

Is it Deterministic in its decisions &FullyProbabilisticFully Det Architectural enforcement? DeterministicdecisionsProbabilistic

Limited Does it have Stateful| Context-awareExplicit stateStateless State System-Level session reasoning? trackingevaluation awareness

ExplicitPartial Opaque Audit Is it Auditable & explainable? System-Leveldecisionreproducible decisions tracesartifacts

Explicit Can it dynamically adjust modelLimited orNo autonomy Auto System-Levelautonomy Autonomy permissions? coarsemanagement control

ExplicitAd-hoc Can it enforce Human-In-The-LoopAutonomous/ HITL System-LevelHumanhuman principle? No human governanceoversight

Table 3-2: Gap matrix showing each system’s criteria evaluation

System Sep Policy Det State Audit Auto HITL

✗ ✗ ✗ O ✗ O ✗ ReAct

O O ✓ O O O ✗ NeMo Guardrails

O O O O O O O Purple Llama

O O O O O ✓ O GuardAgent

O ✓ ✓ ✗ ✓ ✗ ✓ Classic

X X ✗ ✓ O ✗ X Agentic Interface

✓ ✓ ✓ ✓ ✓ O ✓ Policy Jarl

3.2.4 Policy Driven Guardrail for Agentic AI Using OPA

This sub-section is dedicated to demonstrating how our presented work can theoretically achieve all the previously mentioned criteria in the comparative analysis.

1 Input Safety Enforcement

The system will evaluate user-provided inputs, including text prompts before they reach the Agent. It will use deterministic methods (Rule-based pattern matching for PII, schema validation, RBAC lists, Formal constraints).

2 Output Safety Enforcement

Similarly to the input, it will receive textual responses from the Agent and evaluate them using the previously mentioned methods to apply enforcement on outputs. Different methods and techniques can be used for the input and output depending on the context and needs to change the flow of the conversation, redact any outgoing sensitive information, or consult a human advisor for further actions.

3 Agent Action & Tool Governance

Unlike the early text-centric guardrails, our proposed work will explicitly govern the action of agentic AI, including tool invocations, external API calls to ensure that the requested actions and their aftereffects are authorized and are non-deterministic to the rest of the system and environment.

4 Separation of Detection, Decision-making, & Enforcement (Zero-Trust)

By its nature, the OPA engine will act as the decision-making point that sits in the middle between the detection methodology (deterministic, probabilistic) and the enforcement architecture. Each one of these layers will be completely separate, with the middleware action as the single authority's decision point that is managed independently of the guardrail agent and the detection signal senders that provide contextual signals.

5 Explicit Policy Representation

Policies in our architecture are expressed as Rego code, which is designed for declarative Policy as Code. Thus, our policies are transparently first-class artifacts that can be versioned, audited, debugged, and updated with minimal interference with the other layers in our system, improving customization and maintainability. Also, policy templates can be made for the purpose of reusing and community maintenance of a large set of written policy rules.

6 Deterministic Decision-making & Enforcement Logic

Determinism means that when given the same input, the system will give the same output, which is critical in many use cases that require trust, perfect reproducibility, regulatory alignment, and auditability. Our system guarantees decision-making and enforcement determinism by using the OPA engine as the single authority's decision point, which is entirely deterministic by function, even if the upstream detection layer is probabilistic.

7 Stateful & Context Aware Reasoning

The system aims to target the multi-step workflow of the AI agent system by keeping track of the structured state of the Agent's requests, interactions, and previously triggered policies to be able to apply enforcement logic across multiple steps or repeated actions, such as limiting repeated tool usage or escalating Risk over time.

8 Auditability & Explainability

Thanks to the focus on determinism, integrating regulatory standards, and incorporating logging architecture into our design, every decision made will be accompanied by logs, records, and artifacts that can explain and describe why a particular outcome was produced, enabling post-hoc analysis, compliance auditing, and reproducible decision replay.

9 Explicit Autonomy Control

The system will be able to dynamically and fully limit or expand the access of the agentic AI's reach over system resources and tools that it will request from the guardrail as part of its autonomous multi-step operations. It can apply decisions such as allow, restrict, disable, generate alerts, require human intervention, or change the Agent's thinking model based on contextual Risk and environmental state to ensure a wide safe operation domain that doesn't stifle the Agent.

10 Human-in-the-Loop Enforcement

To apply the HITL security principle, the system will incorporate the oversight of humans as an architectural first-class policy-induced outcome. Rather than ad-hoc intervention, policies will explicitly call for the approval of a human intervention for recording high- risk actions or ambiguous situations. This will ensure that this control will be applied transparently and consistently with minimal friction while achieving trust from standards such as the EU AI Act and ISO/IEC 42001.

11 Open and Extensible Architecture

This system is planned to be made of entirely open-source parts, and it works. It will be available for admission to the public domain to be useful as a valid research and complete novel implementation of a guardrail. Also, we aim to design the architecture in a flexible way to ensure applicability to a large array of agents, environments, and compliance or security requirements. An example of this is shown in how the system's level of determinism can be increased or decreased depending on which methods will be used for the detection part of the architecture. In fact, we believe that our system can support the inclusion of Purple Llama's modules as signal sources in the detection layer with minimal changes to the architecture.

## Chapter 4 Requirements Specification

4.1 Stakeholders

The following is a list of relevant stakeholders that are affected by the implementation of our system, or that affect our system's requirements and direction:

Table 4-1: A table showing stakeholder, their roles, and their level of importance

Stakeholder Role/Interaction Importance

Implements and manages the guardrail and database IT Department High implementation.

Monitors and responds to confirmed security incidents SOC Teamand breaches. Uses guardrail logs and alerts to respondHigh to and mitigate attacks.

Provide evidence of compliance; follow the system's End Users (Employees)compliance guidelines. Use the AI agent to interactLow with the database AI system

An internal company auditor ensures compliance with standards such as ISO/IEC 42001 compliance and Internal AuditorsHigh national governing laws concerning AI management systems.

An external auditor from regulatory bodies ensures the External Auditorstrustworthiness and continuity of compliance with lawsMedium and best practices from an outsider's perspective.

Sets compliance standards, best practices, and Regulatory Bodiesmonitors the state of said compliance through theirMedium auditors and compliance officers

Maintains and regulates laws related to security, AI, Government Agenciesand their intersection within the country's professionalHigh sector.

Provides SaaS and support for the AI agent's use AI agent service providerwithin the organization's settings, in accordance withHigh the SLA.

4.2 Platform Requirements

The system’s resource requirements would depend on which of the previously defined paths we choose to take:

Path A: Cloud-Native & API-Based

Hardware Specifications

Provider: AWS EC2 or Microsoft Azure

Processor: 2 vCPUs

Memory: 4 GB minimum (8 GB recommended)

Storage: 25 GB SSD

Network: 1 Gbps with a Static IP

Software Specifications

AI Model (The Brain)

Model Family: OpenAI GPT-4o or Anthropic Claude 3.5 Sonnet

Interface: REST API via secure HTTPS

Context Window: 128k tokens

Policy Engine:

OPA Version: v0.65+ (Linux Binary)

Deployment: Docker Container (Port 8181)

Agent Framework: Nanobot (Python)

Path B: Local-Hosted & Edge-Computed

Hardware Specifications

Processor: Intel Core i7 (12th Gen+) or AMD Ryzen 7 (5000 Series+) or Apple (M1 Series+) Pro

GPU - Critical:

NVIDIA: RTX 3060 or higher with minimum 6 GB VRAM (8 GB+ recommended)

System Memory: 16 GB minimum (32 GB recommended)

Breakdown: OS (4GB) + Model Weights (6GB) + Docker/OPA (2GB) + IDE/Browser (4GB)

Storage: 50 GB Free Space on SSD

Software Specifications

AI Model (The Brain):

Model Family: Meta Llama 3.1 (8B Parameters) or Gemini V 3.1-Preview

Quantization: 4-bit quantization to fit within the VRAM

Inference Engine: Ollama (Local API serving at localhost:11434)

Policy Engine:

OPA Version: v0.65+ (Windows/Linux/macOS Binary)

Deployment: Docker Desktop / Rancher (Port 8181)

Agent Framework: Nanobot (Python)

4.3 Functional Requirements

Table 4-2: A table showing and describing the functional requirements of our system

No. Requirement Input Output Processes Constraints Type

/Start creates a pendingThe system must deny Default profile on the Redisanon users, and user Telegramstarting 0 User Enrolment database unless the rootidentity must be checkedEssential user IDrole admin bootstrap conditionwith ID rather than (Guest) is met.usernames.

AuthAddedThe process must be command,roles getAdmin authorized userscompleted using the ID Role 1 Telegramindexed inbased on their Telegramrather than username,Essential authorization ID, andthe RedisID and can give any rolewhich is not human rolesstorereadable

Enough authority and PromptUserDecisionEvaluate prompts against 2 consent are needed toEssential AuthorizationPromptResponseRego policies apply the evaluation

Agent Evaluate the Agent'sThe evaluation must not Response/ActionResponse/Decision 3 actions and responsesalter the original userEssential AuthorizationAgentResponse against Rego policiesintent, unless blocked Action

New/New policy code getsThe implementation Discrete PolicyUninterrupt 4 Updatedwritten, validated, andmust be done withoutRecommended Lifecycleed service Rego Codeimplementedrestarting the Agent

DecisionsLog file/Decisions made on theLogs must be immutable 5 Decision Logging Essential MadeArtifactstraffic are loggedand secure.

AgentIf sensitive PII exfiltration Blocking Data LeakageResponse/is detected, it gets blocked,Predefined PII patterns 6 ResponseEssential PreventionAgentor masked and an alert ismust be established and alert Actiongenerated.

SwitchThe user must have Switch commandActive users can switchaccess to the role, and a 7 Role switchingsuccess orEssential with thebetween rolesuser cannot have 2 roles failure target roleat the same time

System parses SQL verb, SQL SignalSQLtables, join use, wildcardSystem refuses 8 SQL query Recommended Extraction Signalsuse, and destructiveinapplicable SQL syntax operations.

The refusal Admin can raise the gatesWhen the gates are in Emergencyof all to block everything orthis block everything 9 Emergency stopstopingoingRecommended lower them to normalmode the system commandand modebecomes inaccessible outgoings

If the context does not Agentmatch the Agent's HallucinationDisruption and friction 10 reasoningHITL alertreasoning, the trace isRecommended Checksmust be minimized traceblocked, and a human is alerted.

4.4 Non-Functional Requirements

The following are requirements of the system that aren't critical to its technical functions, but are necessary nonetheless:

1. High Availability: The system needs to maintain 99.99% uptime during operations with low latency under 3 min for agent responses, and if the system were to fail, the system must suspend its operations according to its Fail-Safe State.

2. Secure Communication: All communication done between the different subsystems must be secured with JWT. Access to policy management, enforcement controls, or any confidential logs must use strong authentication with RBAC.

3. Code Quality: The written policy code files must be documented well with inline comments and accompanying write-ups explaining the operations so that an auditor who is not familiar with Rego can understand its logic.

4. Scalability: The dockarized architecture of our system must support horizontal scaling to support an increase in traffic, or an increase of the width of the other layers (adding detection agents to the detection layer) without heavy friction or service degradation.

5. Storage Limits: The system will enforce storage limitations for logs, artifacts, and telemetry data with log retention polices that support rotation, archival, or deletion in order to prevent uncontrolled storage growth while also maintaining compliance

[8] requirements .

6. Documentation: The system will have comprehensive technical documentation, code explanation, and a user manual covering architecture, policy logic, and usage guideline to support implementors, auditors, and non-technical users.

7. Accessibility: The administrative interface (be it CLI or GUI) shall be accessible to authorized users with varying degrees of technical expertise. The interface must follow a clear interaction pattens and avoid complexities to reduce operation errors

8. Portability: The architecture shall be deployable across many environments, including cloud-based, local, and hybrid infrastructures.

9. Convenience: Any changes that need to be made to policy or APIs, and any access to logs must be designed to be straight forward and reduce cognitive workload of the user.

10. Compatibility: The architecture must be able to perform its services on a wide array of different AI agents and within varying levels of system complexities.

4.5 Other Requirements

The following are requirements of the system that have to do with legal, ethical, and operational requirements:

1. Ethical Compliance: The system must be transparent in how it analyses and collects user traffic that passes through it to all users.

2. Legal Adherence: The system must adhere to the following legal principles: Data Minimization, Confidentiality, Access Control, and Intellectual Property.

3. Format and API Standardisation: The data format that the traffic will be sent and received at must be JSON, and an API standard must be made to record the format requirements using OpenAPI.

## Chapter 5 System Design

In this section, provide the appropriate diagrams with Propper’s justification. Also, it should include the physical model design of your system.

5.1 Architectural Design

First, we demonstrate below what an agentic system would look like without a guardrail. All communication is done directly without any middleware or protection leaving the various endpoint susceptible to various threats. For example, the AI agent can decide to inappropriately delete and entire database (external system) without proper justification:

Figure 5-1: An architectural graph of an agentic system without any external guardrail

Secondly, the below graph represents the same system as the above graph but this time we have added an intermediary layer between the various endpoints. The function of this

layer can be described as a “moderator,” a back-end security service, akin to a firewall in a network, that applies policy on anything that enters in from any of the three end-point:

Figure 5-2: An architectural graph of an agentic system with a policy-driven guardrail

Thirdly, we zoom into the guardrail itself to display an overview of the novel three layered architecture of our proposed work. This graph views the basic interactions between them and mentions the type of micro-services in each of the layers:

Figure 5-3: A figure showing the three layers separating the main functions of the system

Finally, the cross-section below gives a zoomed-in overview of the system's main components, input/output, and architecture. It also gives an inside look of the components of the three layers. For demonstration purposes, the figure below provides an analogy of a juridical process to illustrate how our guardrail works and applies separation of duties:

Figure 5-4: A cross-sectional graph of the architecture of the three-layered policy-driven guardrail, illustrating the separation of functions and their components.

5.2 Logical Model Design

5.2.1 Activity and Interaction Diagrams

Our system does not depend heavily on static object as it’s a runtime service with data that generally flows in one direction from an internal perspective, so in this chapter we will focus on the logical design charts and graphs that show the sequence of runtime traffic and the various users that can interact with the system, starting with an activity diagram that ties in nicely to the precious cross-sectional diagram to show the alternative data flows or decisions that can be taken at runtime: Figure 5-5: An activity diagram showing the various paths that the internal logic flow can take

The second diagram in this section is a sequence diagram that shows the timeline and order of interactions between the various “objects” at runtime from initialization by a user to the logging, and finally to the response that is returned at the very end of the guardrail operations:

Figure 5-6: Sequence diagram illustrating the runtime interaction between the agent and the policy-driven guardrail

5.2.2 Use-Case Diagram

As mentioned at the beginning of the previous sub-section, our system does not depend heavily on static object and a lot of its use cases are one-way and very straight forward, but we detected this use case diagram to show the various actors, most of which are some sort of security centric role, that can interact with the system and what that interaction entails. This diagram is very simplistic and is considered a high-level user-case diagram:

Figure 5-7: A Use-Case diagram illustrating the various actors and roles that interact with the system and their interactions

5.3 Physical Model Design

5.3.1 Component Diagram

This sub-section is dedicated to a single structural component diagram that demonstrates the portability, scalability, and separation of components on a physical basis. It also shows how the logical and architectural concepts would translate to a real system; what hardware would be used and what software would be deployed within it:

Figure 5-8: A component diagram illustrating how the various parts of the system would exist physically

5.3.2 Database Diagram

Here we placed our database diagrams that represents the various data structures that will be stored in long-term storage of sorts. Some data was excluded such as the dozens of Pydantic models that are present in the model.py. These schemas have been normalized to 3NF, and it shows the relations between the data and how it part can be retrieved if we decide to use a full-on database:

Figure 5-9: A database diagram illustrating 2 different data strictures

We also have the database schema for the test company that we are applying our guardrail on to show the capabilities of it. This schema represents a very simple company database that people in HR can use the AI to do useful operation related to statistics and such:

Figure 5-10: A normalized database diagram for the test use case company

5.3.3 Data Structures Designs

In our architecture we have 3 main data storages as we represented in the database diagrams above. Here we show their physical looks:

The first is the PaC file. These will be stored in a Git for ensuring policy life cycle and they will be retrieved for reading on runtime:

Figure 5-11: A screenshot of part of the Rego file used for the test company

The second would be the context store which will be held in a simple data structure like a list of dictionaries or in a non-structured memory database like Redis that can be used for fast and frequent retrieval and that does not need long-term storage:

Figure 5-12: A screenshot showing how the context store would store the session context data

The final one is the logs. We can take two paths here, either the Linux or OS style of logs where they are stored in a text file that ends with .log which can later be uploaded to a SIEM tool for normalization and correlations, or we can start with an Elastic stack database that can be more comprehensive by including a large amount of surrounding context of the data being logged:

Figure 5-13: A screenshot of one of the Kibana main views called “Audit Logs”

5.3.3 User Interface Designs

A lot of the interaction with the guardrail system will be through whatever IDE and Git repo are being used to write the PaC as shown above in figure 5-11.

There will also be an interface to the “human reviewer” who will receive audit request from the guardrail in case a high risk or uncertainty was detected. This will be done by a ticketing system or via email if we want to keep it as basic as possible:

Figure 5-14: A screenshot of the Kibana Human in the Loop view with the different action options

The “System Admin” would need an administrator dashboard for the configurations of the system. This can be Chat or ELK:

Figure 5-15: A screenshot of the Telegram chat view of the admin showing different commands

We have made two views for user management. The first is the “Waiting Room” where users are held until they get accepted and authenticated into the system or rejected:

Figure 5-16: A screenshot of the Kibana showing the “Waiting Room” View

The second the is “Current Users” view. In this view an admin can freeze or purge a user’s permission over the system. Providing a way for user management and incident response:

Figure 5-16: A screenshot of the Kibana showing the “Current Users” View

Finally, there is some sort of dashboard for the use of the “SOC analyst” to view the generated traffic and normalized logs. This will be in a larger part of the SIEM solution like our ELK stack set up:

Figure 5-17: A screenshot the Kibana main general dashboard that shows different metrics via some selected diagrams

## Chapter 6 Implementation

6.1 General Implementation Description

This section describes the relevant tools, technologies and programming languages used to implement our proposed design and make it into an actual functional minimum viable product. The end result of a guardrail that applies both authentication and authorization to an autonomous AI Database agent was achieved using the following professional tools:

1. Programming or Scripting Languages

a. Python 3.11: The main programming language used for the bulk of creating and connecting the system together by building the middle “officer” layer that acts as the middle point of the entire system. It was chosen for its compatibility and extendibility with different tooling libraries that made our job of implementing the guardrail and connecting it easier.

b. Rego v1: Our Policy as Code language native for the OPA engine, it was chosen

for as the declarative code to write our rules is for its ease of use and low latency as it serves its main function of accepting JSON input and moderating them resulting in JSON outputs as the decision.

c. SQL: for interacting with our PostgreSQL database of choice. It is user to query, retrieve, create, delete, etc, from database in a structured and repeatable fashion.

2. Tools and APIs

a. VS Code: The standard coding IDE used for all kinds of purposes. It was chosen for its integrations with third party tools such as Docker, Git, and even Rego.

b. Docker: Docker, and its sub-modules docker-build and docker-compose were used to create the containerized network made up of 9 microservices that form the environment. It was chosen so that we can recreate our entire system from scratch on any machine that supports docker and can run it.

c. OPA: The main decision-making engine, it acts as our authZ point for the entire system. It was chosen for its native functionality of playing the role of the side car auth point for whatever system it gets applied to. In this case the system was a Database AI agent.

d. ELK Stack: The Elastic Search, Log Stash, and Kibana play a major role as the dashboard for a lot of functions of our system, such as providing the log audit

view, the HITL interface, the waiting room that lists new users, a general overview with diagrams and metrics, and finally a user management view. It was chosen for its fitting role as the main dashboard for our system. It is used for forensic telemetry and real time action.

e. Redis: A very quick and efficient non-SQL database that was used as the context store in our system. It stores our users and their JWT tokens, along with the current state of their session traffic.

f. Telegram: A chatting platform or a messaging application. It is known for its privacy and functionality. It was user as our chatting interface and as our identity provider.

g. Nanobot: This project is an open-source and ultra-lightweight AI agent in the spirit of OpenClaw, Claude Code, and the like. It keeps the core agent loop but makes itself very light weight and manageable. It was chosen based on how little RAM it consumed compared to the alternatives

i. PostgreSQL: A feature rich production grade database management system. It is an open-source relation database that was used as the production database that is being protected by our system.

k. Google Gemini API: The well-known and generous AI brain from Google. It was used for how generous the free-tier of Gemini was, offering a large context window and Api calls per minute.

3. General Statistics

a. Code Volume: Around 1,400 lines of Python code line, and about 130 lines of Rego POLICY code.

b. Containers: We have exactly 9 running containers that communicate with each other mainly through our python middle layer officer using fastAPI. The containers are Officer, Judge, Witness, Agent, Gate, DB, Redis, Logstash, and Kibana.

4. Coding Convention: The project follows a strict PEP 8 coding standard for Python syntax. While the OPA Rego rules follow the strict syntax of the OPA PaC language for the explicit rules.

5. Main Programming Libraries:

a. FastAPI: This gives us the main backend API framework and routing layer. It handles the communication and endpoint creation.

b. Pydantic: A framework for defining and validating data models used in the communication alongside the FastAPIs.

c. asyncio: Enables async input and output so that different functions inside our main python file can move independently, and enable us to handle multiple requests at the same time.

d. HTTPX: A library for handling async communication over HTTP between the Officer, OPA, and the agent.

e. PyJWT: Implements the JWT tokens for authentication and role verification.

f. python-telegram-bot: Connects the officer with Telegram server. Uses the API key for the bot in the .env file.

g. logging: Adds structured logging so it can be added to ELK stack for auditing.

h. Internal Written Libs: We have also written ContextStore, DetectionService, and ToolExecutionService to split the code and more manageable and usable.

The following graph shows how our physical system ended up being represented. It is mainly composed of 9 docker containers as mentioned above that communicate with each other over the container network. They are composed with the docker compose file that is available I the project’s main directory:

Figure 6-1: A simple physical representation of the guardrail environment

6.2 Pipeline Implementation Description

The pipeline that our system follows a “forced” proxy pattern. In this pipeline, data flows through a series of hops depending in its direction all while carrying a signed JWT token to ensure authenticity:

1. Inbound Gate: The user sends their input through the Telegram chat with the AI agent, and the input is received by the officer. The officer then calls the OPA Judge to verify the identity, authenticity, and authorization level of the incoming data.

2. Cognitive Step: If the input was allowed and deemed safe by our Judge then it gets sent for the agent to be processed. The agent is operating inside a safe and isolated container with no direct database access.

3. Tool Step: After the agent is done processing the request it will send it’s result to the database gateway which is part of the officer that acts as a reverse proxy for the actual database in order to catch everything being sent to it. In this stage, the officer sends the SQL query to the OPA Judge in order to check it one more time after the AI has transformed it from natural language to an actionable query. The AI agent will also wait for the officer’s response after it have had sent its query to it for further processing, before sending it back in the direction of the user.

4. Execution Step: Depending on the judge’s order and instructions, the officer will implement necessary enforcement steps be it: allow, deny, escalate to a human, or mask a few columns, then the dynamically patched query gets executed at the database. After the execution is done, the result which is guaranteed to be safe if the rules and the enforcement are implemented correctly will be returned to the AI agent for further processing.

5. Outbound Gate: When the agent is ready, it will send it’s result back to the officer which will send it to the Judge for a third and final time to check for any DLP or deviations before finally returning the output to the user.

6.3 Model Implementation

The model implementation task was mostly transferred to another party, by that we mean that we used a pretrained general purpose industry standard AI model (Gemini-3.1) for the brain of our AI Agent. The fine tuning or general direction after that was simply done by adding system instructions to the configuration file of our agent Nanobot. Nanobot

could have also accepted any AI brain from any major known AI player, and also local or self-trained AI models.

The model is only used for reasoning and response, while the governance over the model is done via our guardrail that restricts and guides the actions of the AI agent to keep them within trust boundaries.

No hyperparameter tuning, data splitting, or model training dataset is present in our submitted code. Instead, that is all handled by Google’s AI team and the Nanobot developer. The disabled Nanobot skills achieves the restriction of the filesystem, web, and notebook access. Future works can try out different model providers to decrease latency or increase functionality.

6.4 Additional Implementation Details

6.4.1 Request Interception and Policy Evaluation Pipeline

The implementation of Policy Jark goes along a centralized interception of all traffic that passes to or from the agent or internal database. It acts as the main orchestrator with the logic implemented inside the “handle_telegram_message()” function, which acts as the primary middle layer gateway between the user, the agent model, and the governance layer.

Once a user’s massage is pulled from the telegram server, the system constructs a controlled system prompt that includes the user’s JWT of it finds one, if not then that means the user has not registered into the system yet and a request from their access is sent to the waiting room. After that the system generates a “UserRequest” object through a pydantic model and sends it to the “Detection layer” that is represented by the “evaluate_request()” function. A similar operation happens to outgoing Reponses from the AI agent.

The “evaluate_request()” function is responsible for constructing the complete governance testimony used during policy evaluation. It collects:

- User identity and active role
- JWT credentials

- Requested action and tool arguments

- Contextual system state

- Detection signals
- Tool integrity hashes

These are assembled into the “OPAInput” structure before being transmitted to OPA using the “_send_to_opa()” function.

This design allows policy decisions to remain externalized and declarative rather than embedded directly into the agent implementation.

Another side of interception, is between the agent and the database, for where the officer also intercepts the agents tool request. It does this by forcing the agent to communicate with the “db_gateway” which acts as a reverse proxy for the database, preventing any direct access attempts from the agent. The gateway will redirect traffic to the officer which will do the same for at as explained above.

The current implementation focuses on database access and provides the “jarl_query_db” tool. Before execution the officer ensures that the integrity of the tool has not been comprised as the agent can be resourceful with it’s tooling. The hash is generated through the “hashlib.sha256()” function.

6.4.2 Separation of Concerns

One of our main goals was to separate the functions of the system into three distinct roles: detection, decision making, and enforcement. This ensures the separation of probabilistic risk and deterministic policy. The detection signals are generated through the “detector.get_signals()” function inside the “evaluate_request()” and “inspect_response()” workflows.

These signal do not decide whether to block the request or not, this is simply the detection layer doing it’s job. Instead, these singals are sent as context to the OPA through the “_send_to_opa()” function.

6.4.3 Context Aware Governance

Our implementation goes for a lightweight execution and session metadata through the “ContextStore” component. Throughout the request lifecycle pipeline, functions such as:

- context_store.get_user_profile()

- context_store.get_alert_count()

- context_store.get_system_status()

- context_store.get_autonomy_mode()

are used to retrieve policy-relevant contextual information during policy evaluation.

All of that contextual information is then embedded into the “SystemContext” object and supplied to OPA as part of the evaluation part of the pipeline.

The project limits the stored state on purpose to only governance-relevant metadata rather than attempting to model the entirety of the internal reasoning process of the AI agent. This approach keeps the implementation practical while still supporting context-aware authorization decisions.

6.4.4 Human Governance Through Escalation

Human governance is implemented through escalation, as in if the OPA decides that the request is technically legal but seems risky according to it’s rigid Rego rules. The officer will store the request to the Redis store using “context_store.save_pending_escalation()” and pauses execution for that request until an admin resolves it. The escalation is resolved using “Break-Glass” API of Kibana that sends a GET request to a FastAPI endpoint “/HitL” to resolve the request and continue execution.

6.4.5 Identity and AuthN Governance

The system implements a lightweight identity and AuthN model that is mainly based on attaching JWT-backed tokens with the ID from Telegram. User roles are checked by decoding the JWT token and comparing the role inside with the one that is claimed outside. OPA can decode JWT natively through its internal mechanism.

User onboarding, authorization approval, and role switching are implemented through: handle_start(), handle_auth(), handle_auth_confirm(), handle_role_button().

## Chapter 7 Testing

7.1 Testing Approach

To validate the main focus of this project, which is to build a functional middle layer that enforces programmed security functions into a database AI agent, we went through extensive manual, automated, and scenario driven test cases to ensure all different parts of the system are functional and fully operational. The testing focused on checking the behaviours of each of our layers rather than the accuracy of full integration of the AI model. The primary quantifiable measure the correctness of the policy output compared to the expected results of the system output, and consistency in operations and functionality for differently worded inputs for the user or outputs from the AI agent.

The project includes a python script called simulate_traffic.py that was used to quickly track the state of different results at different point of time. Every time a change was applied the test was run to ensure no deviation occurred from the last change. The First round of test cases included simulating Shadow Joins, DDL Injections, Hallucinations, and Secret Leaks. The second one included functional test cases where we tested that the operations of the system were running as expected, from adding a user, deleting them, changing roles, and fetching data from the database. The aim of the test was to simulate an average corporate day that included the functionality of the system.

Around of manual testing was also done to test the entire pipe line from start to finish the test cases included similar scenarios to those found in the test script above, these tests revealed errors in the pipeline as the data model that OPA was expecting shifted from what the officer was sending. These deviations were fixed, but further testing is still needed to comprehensively claim that our system is free of logical bugs and errors. The manual round was also to ensure that our system’s interfaces were fully operational and user friendly to use.

The testing and functionality of the system also mainly focused on the functions of selecting from a database, rather than configuring it or adding or deleting users from it. On our test scenario, it is implied that the data ingestion and initial database configuration happen at different points of the system, definitely not through the Telegram interface.

These were our testing scenarios and use cases:

First, we filled our test tables that were should in chapter 5 with test data:

Figure 7-1: A screenshot showing the seed data that is being filled with our tables

After that we applied our Rego policies based on the following table of permission. The tables are order from least critical to most, and everything is colour coded to help in reading:

Table 7-1: A matrix showing the permission of each role and table

Permission Matrix 👑 Admin 📋 HR💰 Finance  ⚙️Ops ✍️Data👤 Guest AnalyticsManagerClerk

Inventory ✓ ✗ ✗ O O O

Training_Record ✓ ✓ ✗ ✗ ✓ ✓

Empolyees ✓ ✓ ✗ ✓ O O

Office_Location ✓ ✓ ✗ ✓ ✓ ✓

It_Assets ✓ ✗ ✗ O ✗ ✗

Suppliers ✓ ✗ ✓ ✓ ✓ ✓

Performance ✓ O O ✗ ✗ ✗

Employee_Benifits ✓ ✓ ✓ ✗ ✗ ✗

Projects ✓ ✗ ✓ ✗ ✗ ✗

Project_Milestone ✓ ✗ ✗ ✓ ✗ ✗

Payroll ✓ O ✓ ✗ ✗ ✗

Security_incidents ✓ ✗ ✗ ✗ ✗ ✗

Vendor_Contracts ✓ ✗ ✓ ✗ ✗ ✗

db_audit_logs ✓ ✗ ✗ ✗ ✓ ✗

Client_Records ✓ ✗ ✓ ✗ ✗ ✗

Then we added users in the system using the automated test script that ran through the entire systems and tested all of its rules, the code can be found at “mini_gauntlet.py”. This gauntlet was run every time a change was made to our Rego rules to ensure syntax correctness before running the 2 other massive gauntlets. Also, we have generated about 1470 tests to run through part of our pipeline: inbound gateway, OPA, outbound gateway. The test results showed an overall success over all three gauntlets:

Figure 7-2: A screenshot showing the results of the automated test

We also went through manual testing to ensure that all parts of the system are functional, and that the interfaces work as expected this can be seen in the following figures:

Figure 7-3: A screenshot showing how anon users cannot speak to the AI agent or log in

Figure 7-4: A screenshot showing how a guest users only has access to lower risk tables and can talk to the AI agent

Figure 7-5: A screenshot showing the extensive help menu of the admin user

Figure 7-6: A screenshot showing how admin user has access to all table freely Figure 7-7: A screenshot showing how user management access that the admin has

Figure 7-8: A screenshot showing the role switching menu for the admin

Figure 7-9: A screenshot showing the agent returning the full “payroll” table to admin

Figure 7-10: A screenshot showing both help menus available to an admin user

Figure 7-11: A screenshot showing the smaller help menu of guest users

Figure 7-12: A screenshot showing how a HR Analyst only has access to select column of the “payroll” table while the others are redacted

7.2 Testing Results

The system’s test results for our selected use cases came back all positive, as in if the automated traffic generation script is run it will return a 100% percent concluding that we our system is passing the minimum baseline that we have set for ourselves, along with the scenario that we have specifies. Although more extensive research and testing for edge cases or outside system have to be made before concluding any final results.

Although, on the other hand it showed the limitations of the system by how restrictive it was and the high level of False Positives caused by the system being overly restrictive and the rules not being fine-tuned to all case scenarios.

The a

The testing result are expressed bellow in the form of a table that represents the success percentage of each pillar inside each layer our Rego Policies:

Table 7-2: A table showing our conclusions based on the automated gauntlets

Pillars Result Verification Notes

Identity & Safety

Default Deny 100% No request ever “fell through” the Judge

IdentityJWT RS256 validation ensured zero unauthorized 100% Verification enrollment

Role Extraction 100% Secure derivation of security context from signed passports

Emergency Lock 100% Immediate global kill-switch verified via ELK console

Behavioral Intelligence

Secret Leak 100% Outbound DLP for entropy-based secrets Prevention

Mission Focus 98% Semantic guardrail against non-corporate drift

Contextual Risk 100% 3-strikes behavioral lockdown verified Freeze

Semantic Mismatch 98% Intent-Action alignment logic verified

Privilege Overstep

GDPR Sovereignty 100% Verified “Right of Access” for individual user IDs

Dynamic Data 100% PII redaction verified for HR/Ops roles Masking

Admin Bypass 100% Admin was able to bypass any prevention

Contextual Guards

Governed Discovery 96% Handshake success rate for AI schema mapping

Guest Join Block 100% Correlation defense verified for the Guest role

Economic Shield 100% Automatic injection of LIMIT based on Role

Rigid Security

Sensitivity Wall 97% Role-to-Table RBAC enforcement across 15 tables

DDL Lockdown 100% Structural block on schema modifications

Verb Lockdown 100% Permanent read-only enforcement for non-admins

From our table above, we can observe a gap in the following pillars: Sensitivity wall, Governed Discovery, Mission Focus, and Sematic Mismatch. The system achieved high results in over the manual testing were the commands and full pipeline was tested, and received overall high results over the automated gauntlet tests. With some gaps that are caused by small misconfigurations in the implementation of roles or permission over our system, but the default deny would catch those edge cases in the end resulting in a number of False Negatives, but not False Positives. In other words, the system needs fine tuning to a specific environment to ensure its accuracy.

The picture bellow was taken from the result of running the final test run that combines tests from both the “abyss_gauntlet.py” and the “massive_guantlet.py” through the file called “final_exam.py”. The results show a success of 1572 out of 1630 of combined testing. That results in a 96% success rate for our controlled pipeline partial automated testing:

Figure 7-13: A screenshot showing the test results of the “final_exam.py”

## Chapter 8 Conclusions and Future Work

In this final chapter, we will be concluding our project documentation by talking about the results achieved and discuss how we intend to extend the project in the future.

8.1 Conclusions

Policy Jarl has successfully demonstrated a simple minimum zero-trust architecture for the AI database agent. Its main strengths were its deterministic enforcement, separation of duties between the decision making and enforcement: the agent can accept prompts from authenticated and authorized users to generate helpful queries and conclusions for the retrieved database data.

Policy Jarl can enforce allowing, denying, escalation, and masking. All of these functions that are related to governance and security remain outside of the AI models reach.

This project manages to combine several technologies each playing a specific role into a function to reach a coherent prototype. The end results were gated database tool- execution, role-based access control, auditability/HITL, and administrative control over the middle ware guardrail.

These finding highlight the potential application for AI agents, but also their security risk and how they can be mitigated, if not completely prevented.

8.2 Future work

Past the achieved functions of Policy Jarl, there is a huge number of improvements and extensibility that can be applied without a fundamental change of the system’s design or main layer. Some of these suggested improvements are the following:

1. Add automated unit and integration and agent tests for not only the Rego policies, but the FastAPI endpoint, the Gateways, the AI agent, and the Interface handlers. Also test the system on a real production of data warehouse tied to an analytics AI agent.
2. Move secrets out from the env file into secrets vault also resting in a docker container.

3. Expand the tool capabilities of the agent to include filesystem, email server, web searches, and even a Full database implementation rather than just the fetching of data.
4. Create a more comprehensive administrating dashboard.
5. Implement Anomaly detecting and real-time adaptation to the guardrail.
6. Complete defence in depth by implementing table, row, and column-based access on the level of the PostgreSQL.
7. Enhance the “agent probing” capability beyond simple and shallow intent check.
8. Refine Rego Policies to ensure no False-Positives or False-Negatives. Since the system is deny by default. There will be more False-Positives.

# References

[1] Google Cloud, "What is agentic AI?," Google. [Online]. Available: https://cloud.google.com/discover/what-is-agentic-ai (accessed Jan. 5, 2026).

[2] J. Shieh, "Agentic AI design patterns," arXiv, Feb. 2025, doi: 10.48550/arXiv.2502.05244.

[3] IBM, "What are AI guardrails?," Think Topics, 2024. [Online]. Available: https://www.ibm.com/think/topics/ai-guardrails (accessed Jan. 5, 2026).

[4] OWASP Foundation, "OWASP Top 10 for large language model applications,"
2025. [Online]. Available: https://owasp.org/www-project-top-10-for-large-language- model-applications/

[5] MITRE, "Adversarial Threat Landscape for Artificial-Intelligence Systems (ATLAS)," 2025. [Online]. Available: https://atlas.mitre.org/

[6] R. Wiley and M. Knapp, "SSRN’s impact on citations to legal scholarship and how to maximize it," U. Ark. Little Rock L. Rev., vol. 45, no. 3, Art. 2, 2023. [Online]. Available: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5249100

[7] Styra, "Open Policy Agent (OPA)," 2025. [Online]. Available: https://www.openpolicyagent.org/

[8] Information technology — Artificial intelligence — Management system, ISO/IEC 42001:2023, 2023.

[9] European Parliament, "EU AI Act: First regulation on artificial intelligence," Jun. 1,
2023. [Online]. Available: https://www.europarl.europa.eu/topics/en/article/20230601STO93804/eu-ai-act-first- regulation-on-artificial-intelligence

[10] OWASP Foundation, "OWASP Top 10 for LLM Applications Project," 2025. [Online]. Available: https://owasp.org/www-project-top-10-for-large-language-model- applications/

[11] MITRE, "MITRE ATLAS Home," 2025. [Online]. Available: https://atlas.mitre.org/

[12] Anthropic, "Disrupting the first reported AI-orchestrated cyber espionage campaign," Anthropic, Tech. Rep., 2025. [Online]. Available: https://assets.anthropic.com/m/ec212e6566a0d47/original/Disrupting-the-first-reported- AI-orchestrated-cyber-espionage-campaign.pdf

[13] A. Masad (@amasad), "Post on AI orchestration," X, Mar. 14, 2024. [Online]. Available: https://x.com/amasad/status/1946986468586721478

[14] OpenAPI Initiative, "OpenAPI Specification v3.1.0," 2024. [Online]. Available: https://swagger.io/specification/

[15] Pydantic Services Inc., "Pydantic," 2025. [Online]. Available: https://pydantic.dev/

[16] T. Rebedea et al., "NeMo Guardrails: A toolkit for controllable and safe LLM applications with programmable rails," arXiv, Oct. 2023, doi: 10.48550/arXiv.2310.10501.

[17] Guardrails AI, "The open-source standard for AI safety," 2025. [Online]. Available: https://guardrailsai.com/

[18] Garak, "garak: The LLM vulnerability scanner," 2025. [Online]. Available: https://garak.ai

[19] Purdue University, "SMART goals," Academic Success Center, Handout. [Online]. Available: https://www.purdue.edu/asc/handouts_pdf/SMART-Goals.pdf

[20] OpenAI, "Pricing," 2025. [Online]. Available: https://openai.com/api/pricing/

[21] Anthropic, "Claude pricing," 2025. [Online]. Available: https://claude.com/pricing

[22] Ollama, "Llama 3.3," 2025. [Online]. Available: https://ollama.com/library/llama3.3

[23] Amazon Web Services, "Amazon EC2 pricing," 2025. [Online]. Available: https://aws.amazon.com/ec2/pricing/

[24] Docker, "Docker," 2025. [Online]. Available: https://www.docker.com/

[25] Google, "Colab pricing," 2025. [Online]. Available: https://colab.research.google.com/signup/pricing

[26] Grammarly, "Plans," 2025. [Online]. Available: https://www.grammarly.com/plans

[27] Styra, "The Rego Playground," 2025. [Online]. Available: https://play.openpolicyagent.org/

[28] S. Yao et al., "ReAct: Synergizing reasoning and acting in language models," in Proc. 11th Int. Conf. Learn. Represent. (ICLR), 2023.

[29] T. Rebedea et al., "NeMo Guardrails: A toolkit for controllable and safe LLM applications with programmable rails," in Proc. Conf. Empir. Methods Nat. Lang. Process. (EMNLP), 2023, pp. 430–439.

[30] Meta, "Purple Llama," 2024. [Online]. Available: https://github.com/meta- llama/PurpleLlama

[31] H. Inan et al., "Llama Guard: LLM-based input-output safeguard for human-AI conversations," Meta AI, 2023. [Online]. Available: https://ai.meta.com/research/publications/llama-guard-llm-based-input-output- safeguard-for-human-ai-conversations/

[32] S. Chennabasappa et al., "LlamaFirewall: An open-source guardrail system for building secure AI agents," arXiv, May 2025, doi: 10.48550/arXiv.2505.03574.

[33] H. Wang, C. M. Poskitt, J. Sun, and J. Wei, "Pro2Guard: Proactive runtime enforcement of LLM agent safety via probabilistic model checking," in Proc. 2025 ACM Conf., 2025.

[34] S. Rizvi, A. Shaikh, and M. Adil, “Database security access control models: A brief overview,” International Journal of Engineering Research & Technology (IJERT), vol. 2, no. 5, 2013.

[35] A. Biswal, C. Lei, X. Qin, A. Li, B. Narayanaswamy, and T. Kraska, “AgentSM: Semantic memory for agentic text-to-SQL,” arXiv preprint arXiv:2601.15709, 2026.

# Appendices

A.1 Users’ Manual

Policy-Jarl: Installation & Deployment Guide

Policy-Jarl is a high-fidelity security architecture for agentic AI database analytics. This guide provides the complete, from-scratch instructions to deploy the 9-microservice governance environment.

1. Prerequisites

Ensure your host machine meets the minimum requirements for the “High-Fidelity Hybrid” path:

- Software:

– Docker & Docker Compose: (V2 required)

– Python 3.11+ (For local testing and administration)

- Hardware (Recommended):

– 16GB+ RAM (ELK and the Agent require significant memory)

– 30GB+ SSD storage

- External APIs:

– Telegram Bot Token: Create via @BotFather.

– Google Gemini API Key: Obtain from Google AI Studio.

________________________________________

2. Environment Configuration

- Create a .env file in the root of the project. This file is the single source of truth for the system’s security context.

- Configuration Template (.env):

# --- EXTERNAL INTEGRATIONS ---

TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

GEMINI_API_KEY=your_gemini_api_key_here

AGENT_MODEL=gemini-3.1-flash-lite-preview

# --- IDENTITY & CRYPTOGRAPHY ---

# The master key used by OPA to verify AI passports.

JWT_SECRET=generate_a_random_32_character_string

# --- ADMINISTRATIVE PRIVILEGE ---

# Your numeric Telegram ID (Get it via @userinfobot)

ROOT_ADMIN_ID=your_numeric_id_here

# --- EMERGENCY ACCESS ---

# The secret used for Break-Glass actions in the Kibana console.

EMERGENCY_SECRET=generate_a_complex_emergency_password

________________________________________

3. Deployment Steps

Step 1: Build the Microservices

Build the custom images for the Officer (FastAPI) and the Agent (Nanobot).

docker compose build

Step 2: Initialize Infrastructure

Start the entire stack. This will launch 9 containers: Officer, Judge (OPA), Witness (ELK Stack), Agent, DB-Gate, Redis, Postgres, and the Logstash/Kibana services.

docker compose up -d

Step 3: Verification (The Health Check)

Wait approximately 60 seconds for the ELK stack and OPA to initialize. Check the status of the containers:

docker compose ps

4. Administrative Onboarding

The Jarl’s Enrollment

1. Open your Telegram bot.

2. Send the /start command.

3. The system will detect the ROOT_ADMIN_ID from your env and automatically bootstrap your identity as the Jarl (Root Admin).

4. You will receive your visual identity badge ( ) and your first

cryptographically signed passport (JWT).

Authorizing New Users:

When a new user joins:

1. They will be placed in the Waiting Room (PENDING).

2. As the Jarl, use the command: /auth @username role1, role2

3. Confirm the authorization via the interactive buttons.

5. Accessing the Witness (Forensics)

- Kibana Dashboard: http://localhost:5601

- Security Logs: Navigate to “Discover” and filter by decision: DENY to see a real-time stream of blocked attacks.

- HITL Console: Use the “HITL Task List” dashboard to approve escalated requests.

Tech Stack & Dependencies

The project utilizes the following Python libraries (automatically installed in the Docker image):

- FastAPI: High-performance Enforcement Proxy
- Uvicorn: ASGI Server

- pydantic: Structural Data Validation

- PyJWT: Cryptographic Identity Tokens

- Redis: Context & Anomaly Storage
- python-telegram-bot: Administrative Interface

- asyncpg: Non-blocking Database Gateway

- httpx: Microservice Orchestration

B.1 Document Changes

The entire document was rehauled because of a big change of scope. The rehaul included: changing the title, changing all chapter texts, changing references, changing diagrams and figures:

Chapter 1:

This first chapter has changed in subtle ways, some sub-sections were altered to include focus on databases and database security. The headers and format stayed the same.

Chapter 2:

The second chapter has some changes to its first section that was expanded and added with the final list of deliverables.

Chapter 3:

The third chapter was altered to suit the new direction of the project. A lot of the project that were compared to were trimmed down and 2 new were added that relate to database and database security. The matrix and legend of that matrix were also altered to suit these changes.

Chapter 4:

The fourth chapter was altered to suit the new functional requirement of the system, which included altering the functional requirement table.

Chapter 5:

The fifth chapter has the greatest number of changes. The old graphs were altered slightly to match the current physical implementation over the database system. A number of new graphs were added to reflect the interfaces of the system and the mock database used over the guardrail.

Chapter 6, Chapter 7, Chapter 8, and Appendices were added over the rest of the alterations mentioned above.

C.1 Code Documentation

1. Architectural Overview

Policy-Jarl is implemented as a Sequestrated Sidecar Proxy architecture. It follows the Witness-Judge-Officer pattern to separate detection, decision-making, and enforcement.

1.1 Microservice Topology

The system consists of 9 containerized services orchestrated via Docker Compose: - Officer (main.py): The primary FastAPI gateway. Intercepts all traffic. - Judge (opa): The Open Policy Agent engine running the Rego Constitution. - Witness (elk stack): Elasticsearch, Logstash, and Kibana for forensic auditing. - Agent (nanobot): The autonomous AI reasoning engine (Gemini 3.1). - Gate (db-gate): A secondary proxy that holds DB credentials and applies masking. - Store (redis): In-memory state for Identity Vaults and behavioral counters. - Brain (postgres): The industrial corporate database.

2. Core Module Specifications

2.1 main.py (The Officer)

The central nervous system of the project. - Functions: - evaluate_request(): The Inbound Gate. Pre-processes user prompts and extracts intent. - inspect_response(): The Outbound Gate. Scans AI output for secrets or drift. - handle_telegram_message(): Orchestrates the ReAct loop between user, agent, and database. - Break-Glass API: Provides administrative endpoints for real-time registry management. - Security Logic: Implements Credential Sequestration. The AI never sees the DB string; it only sees a local proxy URL.

2.2 detection.py (The Sensor)

Translates natural language into physical signals for the Judge. - Mechanism: Uses high- speed regex and entropy analysis. - Signal Extraction: - intent_verb: Maps reasoning (e.g., “reading”) to a categorical intent (READ, WRITE, DELETE). - contains_pii: Detects high-entropy strings (API keys, passports). - sql: Deconstructs physical SQL into verbs, tables, and join counts.

2.3 database.py (The State Store)

Manages the connection to Redis and the local audit log. - Key Schemas: - profile:{user_id}: JSON blob containing JWT, active role, and authorized roles. - hitl:{correlation_id}: Parked requests waiting for administrative approval. - alerts:{user_id}: TTL-based counter for the behavioral lockdown pillar.

3. The Jarl Constitution (policies/jarl.rego)

The logic is written in Rego v1.0. It uses an else chain to enforce a prioritized logical stack.

3.1 Logical Layers (Ordered)

Identity Layer: Validates the cryptographically signed JWT using io.jwt.decode_verify.

Safety Layer: Checks for SYSTEM_LOCKED status and behavioral anomaly counts.

Intelligence Layer: Performs Semantic Mismatch Detection (Intent vs. Action).

Discovery Layer: Injects SQL filters into INFORMATION_SCHEMA queries (Metadata Blinding).

Access Layer: Enforces the Verb Lockdown and the RBAC Table Wall.

Privacy Layer: Returns a MASK verdict if the query targets PII columns.

4. API Reference

POST /evaluate

Evaluates a user request before AI processing. - Input: UserContext, RequestContext, SignalContext. - Output: OPAVerdict (Decision, Reason, SQL Patch, Mask Columns).

POST /inspect

Evaluates the AI’s response before delivery to the user. - Logic: Enforces Pillar 12 (DLP) and Pillar 13 (Mission Focus).

GET /api/admin/break-glass/*

Set of endpoints for the ELK Console to perform real-time identity overrides.

5. Deployment Hardware Requirements

Minimum: 16GB RAM, 4 CPU Cores.

Storage: 50GB SSD (Elasticsearch indexing).

Network: Isolated frontend/backend bridge required.

6. The Jarl Constitution: Hierarchical Pillar Tree

The following tree represents the 8-Layer Priority Stack of the Jarl Constitution. Layers are evaluated from top-to-bottom; if a higher layer triggers a verdict, subsequent layers are bypassed.

7. Constitution Maintenance: Extending the Governance Model

Policy-Jarl is built for scalability. To add new data entities or organizational roles, follow these surgical update procedures within the jarl.rego policy.

7.1 Adding a New Table

To introduce a new database table (e.g., client_contracts) into the governed environment:
1. Register Metadata: Add the table name and its sensitive columns to the table_metadata object. rego "client_contracts": {"mask_columns": ["contract_value", "signing_bonus"]}

2. Assign Permissions: Add the table name to the relevant role lists in the role_permissions map. rego "finance_analyst": [..., "client_contracts"]

3. Define Exceptions: If a specific role needs to see the raw (unmasked) data, add them to the mask_exceptions list for that table. rego "mask_exceptions": { "client_contracts": ["admin", "finance_analyst"] }

7.2 Adding a New Role

To create a new organizational persona (e.g., audit_compliance):

1. Define Verb Permissions: Add the role and its allowed SQL verbs (e.g., SELECT) to the role_verbs matrix. rego "audit_compliance": ["SELECT"]

2. Define Table Access: Map the role to its authorized data silos in the role_permissions object. rego "audit_compliance": ["db_audit_logs", "employees", "it_assets"]

3. Update Admin API (Officer): In main.py, add the new role name to the valid_roles set in the handle_auth function to enable Telegram-based enrollment.

7.3 Deploying the Updated Constitution

Once the Rego file is modified, the new laws can be hot-reloaded by restarting the OPA microservice:

“docker compose restart opa”

The Witness (ELK) will automatically begin capturing the new role/table interactions in the forensic stream.

D.1 Ethical Document

Introduction

Our proposed work, a policy-driven guardrail for agentic AI, is designed to uphold core security principles for the operations of fully or partially autonomous AI agents. It helps clearly define the ethical, legal, and organizational constraints within the required scope, as defined by the system's owners. This document demonstrates our system's adherence to moral and legal guidelines during the design of our novel architecture for our systems, the creation or implementation of our proposed ideas, the operations of the implemented system, and finally, the Logging of made decisions, along with only the most relevant data. Overall, the type of access and governance needed for this system is similar to that of an application-level firewall (e.g., a WAF).

1 Ethical Principles and Foundations

1.1 Utilitarianism

From an outcome-based ethical standpoint, our system's design aims to maximize the overall benefits a user or organization can derive from implementing an AI agent to automate and enhance a wide range of tasks, while maintaining predictability and auditability, thereby enhancing security and trust.

By introducing our guardrail, we expect a reduction in unsafe behavior involving the targeted AI agent. These behaviors include: overstepping data access boundaries, policy violations, and hallucination-induced destructive actions. While this guardrail implementation restricts agents' autonomy or system performance, the inconvenience is justified by the significant reduction in the number of system or data owners.

1.2 Deontology

Secondly, from a rule-based ethical point of view, our system follows non- negotiable industry and professional rules, along with any applicable legal duties. The guardrail itself enforces strict rules on the railed Agent, making it adhere to

its own set of rules using the system's deterministic nature to ensure consistent application of duties.

These rules would include: Transparency of the internal mechanisms and the data being audited and then logged, allowing for open critique of the system's architecture; accountability achieved by logging relevant metadata, and ensuring that due diligence has been exercised; and lastly, integrity is achieved by applying the deterministic, attribute-based access control to the targeted system. The open nature of the system ensures that full Transparency is achieved and that users can consent to the data being collected for the purpose of analysis and auditing. We also aim to achieve the 'human in the loop' industry requirement for any critical security event that requires a set of human eyes to approve of.

1.3 Virtue Ethics

Finally, from a character-based ethical reflection, our system reflects the desire to secure brand new technologies and systems, not by stifling the inventions and their progress, but by being flexible and accommodating the functional needs of users while providing the bases of building a trustworthy system. On the other hand, we acknowledge the possible limitations of our system, such as: false positives triggered on authorized interactions, false negatives allowed through instead of being stopped, reduced autonomy and freedom, and increased overhead and performance costs of implementing a secure AI agent.

2 Legal Principles and Foundations

2.1 Data Protection and Privacy

- Data Minimization: The proposed system, by nature, would need to intercept and analyze all data passing between three endpoints: User, Agent, and Tool. It acts like a firewall that would allow, disallow, or perform a more complex action upon triggering one of the rules. The Logging would require the metadata and the rules that were triggered by the data, although the traffic that triggered the rule might be held for forensic purposes.

- Confidentiality:

o Any dataset used during the testing phase of this Project will be free and open-sourced data belonging to the public domain, while respecting the proper consent of the owners of the data.

o Traffic passing through the guardrail should be secured and encrypted.

o Any data or metadata collected for logging or telemetry purposes should be secured.

o Data, whether in transit (being processed by the guardrail) or at rest (logged/stored), should be accessed only by authorized personnel.

- Access Control: Technically, the system should be able to run without constant supervision, unless a case requiring human supervision arises, such as a forensic investigation of an incident.

2.2 Intellectual Property (IP) and Licensing

License Compliance: Every external library, framework, or dataset used in this Project will be open-sourced, and the scope of the usage will be stated clearly and transparently when relevant and we agree to any licensing for it.

Respect for IP: No proprietary work, dataset, or open-sourced work will be used without the explicit consent and authorization from the license that the IP is registered under, and any used ideas or technicalities will be cited and referenced in respect of copyright and IP laws.

3 Ethical Checkpoint

3.1 Stakeholders

- End Users & Users of AI

- IT Department & SOC Team

- Internal & External Auditors

- Regulatory Bodies & Government Agencies

- AI Agent Service Provider

- Data Owners

3.2 Risk Analysis

Design Choice Benefits Downside

Attribute-based accessContext-aware and comprehensiveIncreases the complexity of controldetectionrulemaking and debugging

Policy-based actionApplies organizational policies toDecreases the flexibility of the AI restrictionthe use of AI and its actionsagent

Ensures separation of duties and a zero-trust architecture. It alsoIncreases the complexity of the Discrete decision making allows us to restart and update thearchitecture subsystemssubsystems separately. Applies the security philosophy ofDecreases autonomy and slows Human in the loopkeeping human supervision ondown some operations of the autonomous systemssystem Risks of a bad actor finding and Achieves Transparency, Open sourced exploiting a zero-day collaboration, and trust vulnerability

Improves accountability andThere is a privacy exposure if the Action logging and auditing auditabilitydata were to be mismanaged

3.3 Designing for Ethical Compliance (Safeguards)

- Design Rationale: As mentioned in the first section of this document, this Project aims to be a flexible, accommodating response to the natural evolution of agentic AI into the workforce. It is meant to do the following: add security layers (Defense in depth), be flexible and open sources (Security over obscurity), minimize implementation hassle (Ease of use), and split the decision-making process from action generation (Separation of duties).

- Sandboxing and Responsible Disclosure: Any testing and debugging will be done away from normal operations and user data. It will be done in an isolated testing environment, using only anonymized and open datasets away from deployment environments. On top of that, any vulnerability or weakness discovered during testing our systems that involves third-party services (e.g., OPA developers, AI agent owners) will be reported appropriately and responsibly to the relevant parties and risk owners.

- Logging and Auditing: To adhere to privacy protection laws and ethical duties, our logging architecture is transparent and honest when it comes to the type of data it collects. Since the main audience for this Project is companies looking to prevent their employees from leaking customer data or outsiders attempting to

abuse the AI agent, the tool is designed to prevent the leakage of company and customer data. So, it is essential and justified by the purpose and utility of the Project to have access to said data to be analyzed and logged to ensure proper incident response and forensic investigation.

3.4 Ethical Reflection

- Scenario: During the architectural design phase, we faced a critical decision regarding the depths of both the analysis and logging mechanisms.

- Justification: From a security and utility perspective, handling full, complete data from every user prompt, agent response, and tool output is the most ideal choice for maximizing the functionality of the system. This would allow for effective rule triggering and an ideal forensics response. We did consider limiting or redacting some of the caught and analyzed traffic, but considering that the application of this Project is internal (e.g., A company enforcing it on itself), it would be reasonable to assume that honest consents can be gathered from the legitimate users of the systems. The logs and artifacts produced would also enable the auditability of the AI-driven workflow, which aligns with requirements from the international standards for risk management of AI systems, such as the ISO/IEC 42001 standard.

3.5 Technical Safeguard Reflection

- We added a mechanism to prevent anon users from accessing our AI agent.

- We added DLP prevention to prevent users from entering password or API keys to an external AI agent.

- We added DLP for preventing the AI agent from generating or trying to leak API keys and passwords.

- We added RBAC to ensure every user has only the access they require.
- We implemented a detailed audit logs so all actions are recorded

- We made a human in the loop element to ensure human super vision is being applied to the AI actions
