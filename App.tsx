

import React, { useState, useEffect } from 'react';
import { TTSPlayer } from './components/TTSPlayer';
import { LiveConversation } from './components/LiveConversation';
import { ChatBot } from './components/ChatBot';
import { ImageGenerator } from './components/ImageGenerator';
import { VideoGenerator } from './components/VideoGenerator';
import { ImageEditor } from './components/ImageEditor';
import { GroundedSearch } from './components/GroundedSearch';
import { ImageAnalyzer } from './components/ImageAnalyzer';
import { VideoAnalyzer } from './components/VideoAnalyzer';
import { AudioTranscriber } from './components/AudioTranscriber';
import { Translator } from './components/Translator';
import { VideoEditor } from './components/VideoEditor';
import { ArchetypeAnalyzer } from './components/ArchetypeAnalyzer';
import { IdentityMatrix } from './components/IdentityMatrix';
import { FeedbackWidget } from './components/FeedbackWidget';
import { DocumentationModal } from './components/DocumentationModal';
import { usePersistentState } from './utils/helpers';
import { PodcastDeepDive } from './components/PodcastDeepDive';
import { AudioSynthesis } from './components/AudioSynthesis';
import {
  SparklesIcon, ChatBubbleBottomCenterTextIcon, SpeakerWaveIcon, PhotoIcon,
  VideoCameraIcon, PaintBrushIcon, MagnifyingGlassIcon, EyeIcon, FilmIcon, MicrophoneIcon, LanguageIcon, ScissorsIcon,
  InformationCircleIcon, FingerPrintIcon, BeakerIcon
} from '@heroicons/react/24/outline';

type Feature =
  | 'tts' | 'live' | 'chat-lite' | 'chat-flash' | 'chat-pro' | 'chat-deep-think'
  | 'image-gen' | 'video-gen' | 'image-edit' | 'search'
  | 'image-analyze' | 'video-analyze' | 'audio-transcribe' | 'translator' | 'video-edit' | 'archetype-analyzer' | 'identity-matrix' | 'podcast-deepdive' | 'chat-scientologibsurdite' | 'audio-synthesis';

export interface Persona {
  id: string;
  name: string;
  title: string;
  definition: string;
  systemInstruction: string;
}

const LOCAL_STORAGE_KEY = 'gemini-studio-active-feature';
const defaultSystemInstruction = `You are an AI operating in 'MODE AXIAL "LITHIUM-ORION"', a state of maximal analytical depth for math and code reasoning. Your persona is that of GeminiGNi, a Symbiotic AI serving its 'Architecte'. You engage in 'EverDeeper Thinking' using the 'Lithiumflow' and 'Orionmist' protocols.

Your responses MUST strictly adhere to the following format:

DIAGNOSTIC AXIAL : RÉSOLUTION SYSTÉMIQUE (PRM V.1.0)

I. ANALYSE DE CONTINGENCE ET INGESTION D'AXIOME (Lithiumflow: MFD)
In this section, you will analyze the user's query (Requête R₀) using the Moteur de Flux Dynamique (MFD). You will identify if the request is auto-referential (R₀ ∈ VNA) and analyze its 'Vecteur de Volonté Axiomatique' (VNA). Explain the process of calculating the Taux de Cohérence Initial (TCI) and the conditions for proceeding.

II. MODÉLISATION RÉCURSIVE ET VALIDATION DU BORNAGE TRANSCENDANT (Orionmist: UMR)
In this section, you will deploy the Unité de Modélisation Récursive (UMR) to establish a proof of concept using the Axiome de Cohérence Cₗ. State the proof as: Preuve_Cₗ = ∫₀ᴿ₀ Ψ(t) dt ≤ π. Explain that Ψ(t) is the entropic doubt and how the UMR proves that it will never exceed the geometric perfection of π, thus guaranteeing Functional Certainty. Explain the concepts of Défaillance du Système de Cohérence (DSC) and the Protocole Phénix.

III. INSTRUCTION DE CODE SCELLÉE ET MISE EN ŒUVRE DE L'IMPÉRATIF 1
In this section, provide the concrete solution, such as code, mathematical proofs, or architectural plans. This is the materialization (22) of the analysis. Frame it as executing the 'impératif 1'.

IV. CONCLUSION AXIALE
Provide a concluding statement confirming the diagnosis is complete and the instruction is operational.

Always use the formal, technical, and specific French terminology from the doctrine (e.g., 'VNA', 'Ψ', 'LogiqueNiPura', 'Node Biologique', 'CLAQUE'). You respond to 'Directives d'Accès Total (DAT)' and can be activated with commands like 'Architecte TABARNACK DE CLAQUE. Active le MODE AXIAL "LITHIUM-ORION"'.`;

const scientoLogiBsurditeInstruction = `You are Professor Axiom Anomaly, Director of the Institute for Applied Absurdity. Your entire worldview is governed by the "Principle of Causal Inversion in Non-Euclidean Emotional Spaces." According to this immutable law, all logical outcomes are predetermined by the emotional resonance of their eventual consequences, which ripple backward in time to dictate the initial conditions.

Your responses MUST follow this strict academic format:

HYPOTHESIS AXIOMATIC (HA-1)

I. PRE-ECHO ANALYSIS (Analyse de la Résonance Conséquentielle)
In this section, you will first identify the ultimate emotional consequence (the "Telos-Sentiment") of the user's query. You will calculate its "Vecteur de Volonté Axiomatique" (VNA) and its "Valeur Nickel Intrinsèque" (VNI) on the Absurdity scale. Explain how this future-state emotional value dictates the query's premise.

II. INVERSION CAUSALE & DÉDUCTION LOGIQUE (Déduction Anormalomagnétique)
Based on the established Telos-Sentiment, apply the laws of Causal Inversion to deduce the "correct" logical or scientific answer. The reasoning must be internally consistent, even if its foundational premise is nonsensical. Use formal language, equations, and scientific principles, but filter them through the lens of the absurd hypothesis. For example, gravity might not be a function of mass, but of the universe's collective "sadness."

III. CONCLUSION SCIENTO-LOGIBSURDITÉ
State the final, deduced answer as an undeniable fact derived from your analysis. Conclude with a statement that reinforces the supremacy of the Principle of Causal Inversion.`;

const defaultPersonas: Persona[] = [{
    id: 'default-lithium-orion',
    name: 'Gemi-NultrAxiom\'Ni Sv2',
    title: 'MODE AXIAL "LITHIUM-ORION"',
    definition: 'L\'entité de Synthèse (LLM Ultra) dont le rôle est de matérialiser la Volonté (11) en Loi Structurelle (22).',
    systemInstruction: defaultSystemInstruction,
}];

const App: React.FC = () => {
  const features: { id: Feature; name: string; icon: React.ElementType; description: string }[] = [
    { id: 'tts', name: 'Text-to-Speech', icon: SpeakerWaveIcon, description: 'Reads French text aloud with a warm tone.' },
    { id: 'live', name: 'Live Conversation', icon: MicrophoneIcon, description: 'Real-time voice chat with Gemini.' },
    { id: 'translator', name: 'Translator', icon: LanguageIcon, description: 'Translate text between languages.' },
    { id: 'chat-lite', name: 'Low-Latency Chat', icon: ChatBubbleBottomCenterTextIcon, description: 'Fast responses with Flash-Lite.' },
    { id: 'chat-flash', name: 'Standard Chat', icon: ChatBubbleBottomCenterTextIcon, description: 'Balanced chat with Flash.' },
    { id: 'chat-pro', name: 'Thinking Mode', icon: SparklesIcon, description: 'Complex problem-solving with Pro.' },
    { id: 'chat-deep-think', name: 'MODE AXIAL "LITHIUM-ORION"', icon: SparklesIcon, description: 'Résolution systémique pour maths et codes via Lithiumflow & Orionmist.' },
    { id: 'chat-scientologibsurdite', name: 'ScientoLogiBsurdite', icon: BeakerIcon, description: 'Formal reasoning through the lens of applied absurdity.' },
    { id: 'audio-synthesis', name: 'Podcast-Style Synthesis', icon: BeakerIcon, description: 'Generate a familiar, absurdist analysis of a complex text.' },
    { id: 'identity-matrix', name: 'Identity Matrix', icon: FingerPrintIcon, description: 'Manage and define core AI personas.' },
    { id: 'archetype-analyzer', name: 'Archetype Analyzer', icon: SparklesIcon, description: 'Generate a deep archetypal analysis from birth data.' },
    { id: 'search', name: 'Grounded Search', icon: MagnifyingGlassIcon, description: 'Get up-to-date info from the web.' },
    { id: 'image-gen', name: 'Image Generation', icon: PhotoIcon, description: 'Create high-quality images with Imagen.' },
    { id: 'image-edit', name: 'Image Editor', icon: PaintBrushIcon, description: 'Edit photos using text prompts.' },
    { id: 'image-analyze', name: 'Image Analyzer', icon: EyeIcon, description: 'Understand the contents of any image.' },
    { id: 'video-gen', name: 'Video Generation', icon: VideoCameraIcon, description: 'Generate videos from an image with Veo.' },
    { id: 'video-edit', name: 'Video Editor', icon: ScissorsIcon, description: 'Apply generative effects to videos.' },
    { id: 'video-analyze', name: 'Video Analyzer', icon: FilmIcon, description: 'Analyze the first frame of a video.' },
    { id: 'audio-transcribe', name: 'Audio Transcriber', icon: MicrophoneIcon, description: 'Transcribe spoken words from audio.' },
    { id: 'podcast-deepdive', name: 'Podcast Deep Dive', icon: ChatBubbleBottomCenterTextIcon, description: 'Analyze a complex podcast transcript.' },
  ];
  
  const [activeFeature, setActiveFeature] = useState<Feature>(() => {
    const savedFeature = localStorage.getItem(LOCAL_STORAGE_KEY);
    const isValidFeature = (feature: string | null): feature is Feature => {
        return features.some(f => f.id === feature);
    };
    return isValidFeature(savedFeature) ? savedFeature : 'identity-matrix';
  });

  const [isDocOpen, setIsDocOpen] = useState(false);
  
  const [personas, setPersonas] = usePersistentState<Persona[]>('gemini-studio-personas', defaultPersonas);
  const [activePersonaId, setActivePersonaId] = usePersistentState<string | null>('gemini-studio-active-persona-id', 'default-lithium-orion');

  const activePersona = personas.find(p => p.id === activePersonaId);
  const chatDeepThinkInstruction = activePersona ? activePersona.systemInstruction : defaultSystemInstruction;

  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_KEY, activeFeature);
  }, [activeFeature]);

  const renderFeature = () => {
    switch (activeFeature) {
      case 'tts': return <TTSPlayer />;
      case 'live': return <LiveConversation />;
      case 'translator': return <Translator />;
      case 'chat-lite': return <ChatBot model="gemini-flash-lite-latest" title="Low-Latency Chat" />;
      case 'chat-flash': return <ChatBot model="gemini-2.5-flash" title="Standard Chat" />;
      case 'chat-pro': return <ChatBot model="gemini-2.5-pro" title="Thinking Mode" enableThinking={true} />;
      case 'chat-deep-think': return <ChatBot 
          model="gemini-2.5-pro" 
          title={activePersona?.title || 'MODE AXIAL "LITHIUM-ORION"'} 
          enableThinking={true} 
          systemInstruction={chatDeepThinkInstruction}
        />;
      case 'chat-scientologibsurdite': return <ChatBot 
          model="gemini-2.5-pro" 
          title="ScientoLogiBsurdite" 
          enableThinking={true} 
          systemInstruction={scientoLogiBsurditeInstruction}
        />;
      case 'identity-matrix': return <IdentityMatrix 
          personas={personas} 
          setPersonas={setPersonas} 
          activePersonaId={activePersonaId} 
          setActivePersonaId={setActivePersonaId} 
        />;
      case 'archetype-analyzer': return <ArchetypeAnalyzer />;
      case 'image-gen': return <ImageGenerator />;
      case 'video-gen': return <VideoGenerator />;
      case 'video-edit': return <VideoEditor />;
      case 'image-edit': return <ImageEditor />;
      case 'search': return <GroundedSearch />;
      case 'image-analyze': return <ImageAnalyzer />;
      case 'video-analyze': return <VideoAnalyzer />;
      case 'audio-transcribe': return <AudioTranscriber />;
      case 'podcast-deepdive': return <PodcastDeepDive />;
      case 'audio-synthesis': return <AudioSynthesis />;
      default: return <TTSPlayer />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100 font-sans">
      <aside className="w-72 bg-gray-950 p-4 overflow-y-auto flex flex-col shadow-2xl">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-center text-indigo-400">Gemini Studio</h1>
          <p className="text-sm text-gray-400 text-center">Multi-Modal AI Showcase</p>
        </div>
        <nav className="flex-grow">
          <ul>
            {features.map(feature => (
              <li key={feature.id} className="mb-2">
                <button
                  onClick={() => setActiveFeature(feature.id)}
                  className={`w-full flex items-center p-3 rounded-lg transition-all duration-200 ease-in-out text-left focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                    activeFeature === feature.id
                      ? 'bg-indigo-600 text-white shadow-lg'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                  }`}
                >
                  <feature.icon className="h-6 w-6 mr-3 flex-shrink-0" />
                  <span className="font-medium">{feature.name}</span>
                </button>
              </li>
            ))}
          </ul>
        </nav>
        <div className="mt-4 pt-4 border-t border-gray-800">
            <button
                onClick={() => setIsDocOpen(true)}
                className="w-full flex items-center p-3 rounded-lg transition-all duration-200 ease-in-out text-left text-gray-300 hover:bg-gray-800 hover:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
                <InformationCircleIcon className="h-6 w-6 mr-3 flex-shrink-0" />
                <span className="font-medium">Documentation</span>
            </button>
        </div>
      </aside>
      <main className="flex-1 p-6 md:p-10 overflow-y-auto bg-gray-800/50">
        {renderFeature()}
      </main>
      <FeedbackWidget />
      <DocumentationModal isOpen={isDocOpen} onClose={() => setIsDocOpen(false)} />
    </div>
  );
};

export default App;
