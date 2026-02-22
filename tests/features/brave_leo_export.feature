Feature: Export Brave Leo Conversations to JSON
  As a user of the ACM system
  I want to export Brave Leo AI conversations to JSON
  So that I can store and analyze them programmatically

  Background:
    Given the Brave browser is installed
    And the export destination directory exists at "~/Projects/ai-conversation-toolkit/exports/"

  Scenario: Successful export to JSON
    Given a Brave Leo conversation exists in the browser
    When the export script is executed
    Then a JSON file is created in "~/Projects/ai-conversation-toolkit/exports/"
    And the JSON file contains a "source" field with value "Brave Leo"
    And the JSON file contains an "exported_at" field
    And the JSON file contains a "messages" array with at least one entry

  Scenario: Export file naming convention
    Given a Brave Leo conversation exists in the browser
    When the export script is executed
    Then the output filename matches the pattern "leo-export-\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z\.json"

  Scenario: Failed export handling
    Given the export destination directory does not exist
    When the export script is executed
    Then the script exits with a non-zero status code
    And an error message is written to the log
