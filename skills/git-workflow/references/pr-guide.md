# Pull Request Guide

## Process

1. **Create feature branch** from main branch using naming convention
2. **Create PR** with clear description and test plan
3. **Update documentation** (README.md) if needed
4. **Merge using squash and merge** strategy

## Branch Naming Convention

- **Features**: `feature/description-of-feature`
- **Bug Fixes**: `fix/description-of-fix`
- **Documentation**: `docs/description-of-docs`
- **Refactoring**: `refactor/description-of-refactor`
- **Testing**: `test/description-of-test`

## PR Structure

### Title

Use the same format as commit messages:

```text
type(scope): concise summary
```

### Body Template

```markdown
## Summary
- Key change 1
- Key change 2
- Key change 3

## Test plan
- [ ] Test case 1
- [ ] Test case 2
- [ ] Test case 3
```

## Examples

### Example 1: Feature PR

**Title**: `feat(auth): add OAuth2 authentication`

**Body**:

```markdown
## Summary
- Implement OAuth2 flow with Google provider
- Add token refresh mechanism
- Update login UI with OAuth button

## Test plan
- [ ] Test Google OAuth login flow
- [ ] Verify token refresh works after expiration
- [ ] Check error handling for failed authentication
- [ ] Test logout clears OAuth tokens
```

### Example 2: Bug Fix PR

**Title**: `fix(payment): prevent duplicate charges`

**Body**:

```markdown
## Summary
- Add idempotency key to payment requests
- Check for existing transactions before charging

## Test plan
- [ ] Verify duplicate submission doesn't create double charge
- [ ] Test idempotency key generation is unique
- [ ] Confirm existing transaction detection works
```

## Tips

- Keep PRs focused on a single concern
- Reference related issues with `#123` notation
- Include screenshots for UI changes
- Update tests along with code changes
- Ensure CI passes before requesting review
