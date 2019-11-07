#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from ROOT import gRandom, TH1, TH1D, TH1F, TH2F, cout, TFile, gSystem, TCanvas, TPad, gPad, gROOT, gStyle, THStack, TLegend, TLatex, TColor, TMath, TStyle

# --------------------------------------------------------------------------
# this is to run on just a small number of events
# --------------------------------------------------------------------------

from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
parser.add_option("-N", "--max-entries", dest="maxEntries", type="long",  default=None, help="Maximum number of entries to process")
(options, args) = parser.parse_args()

gStyle.SetOptStat(000000)
gStyle.SetOptTitle(0)


class ttHAnalysis(Module):
    
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

        # --------------------------------------------------------------------------
        # here we can define some histograms
        # --------------------------------------------------------------------------

        self.h_lep_pt = ROOT.TH1F('lep_pt', '; Lepton p_{T} (GeV); Number of leptons', 100, 0, 100)
        self.h_lep_pt.SetLineColor(1)
        self.addObject(self.h_lep_pt)
        
    def analyze(self, event):

        # --------------------------------------------------------------------------
        # this is the event processing
        # --------------------------------------------------------------------------

        # get the electrons, muon, jets in the event (vectors of variables)
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        
        # select events with at least 2 electrons/muons
        if len(muons) + len(electrons) >= 2:

            # loop over muons
            for muon in muons:

                # get pt, eta, phi from the 4-vector
                pt  = muon.p4().Pt()
                eta = muon.p4().Eta()
                phi = muon.p4().Phi()
                
                # apply minimal kinematic selection criteria
                if pt < 10 or abs(eta) > 2.4:
                    continue
            
                #print "muon pt = " + str(pt) + " eta = " + str(eta) + " phi " + str(phi)

                self.h_lep_pt.Fill(pt)  # fill histogram

            # loop over electrons
            for electron in electrons:

                # get pt, eta, phi from the 4-vector
                pt  = electron.p4().Pt()
                eta = electron.p4().Eta()
                phi = electron.p4().Phi()
                
                # apply minimal kinematic selection criteria
                if pt < 10 or abs(eta) > 2.4:
                    continue
            
                #print "electron pt = " + str(pt) + " eta = " + str(eta) + " phi " + str(phi)

                self.h_lep_pt.Fill(pt)  # fill histogram                

            return True


    def endJob(self):

        # --------------------------------------------------------------------------
        # this is run after the events are processed, here we can make a canvas and draw the histgram
        # --------------------------------------------------------------------------

        c = TCanvas()
        self.h_lep_pt.Draw()
        c.SaveAs("test.pdf")

        

preselection=""
files=["ttHTobb_ttTo2L2Nu_Skim.root"]

p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[ttHAnalysis()],noOut=True,histFileName="histOut.root",histDirName="plots",maxEntries = options.maxEntries)
p.run()
