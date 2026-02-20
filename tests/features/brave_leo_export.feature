Feature: Export Brave Leo Conversations to JSON
  As a user of the ACM system
  I want to export Brave Leo AI conversations to JSON
  So that I can store and analyze them programmatically

  Background:
    Given the Brave browser is installed
    And the export destination directory exists at "~/ai-conversations/"

  Scenario: Successful export to JSON
    Given a Brave Leo conversation exists in the browser
    When the export script is executed
    Then a JSON file is created in "~/ai-conversations/"
    And the JSON file contains a "platform" field with value "brave-leo"
    And the JSON file contains a "timestamp" field
    And the JSON file contains a "messages" array with at least one entry

  Scenario: Export file naming convention
    Given a Brave Leo conversation exists in the browser
    When the export script is executed
    Then the output filename matches the pattern "brave-leo_YYYY-MM-DD_HHMMSS.json"

  Scenario: Failed export handling
    Given the export destination directory does not exist
    When the export script is executed
    Then the script exits with a non-zero status code
    And an error message is written to the log
